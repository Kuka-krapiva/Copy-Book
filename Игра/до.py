import pygame
import sys
import random
from конец import display_result  # Импортируем функцию


# Функция для загрузки случайных строк из файлов
def load_random_lines(*filenames):
    try:
        lines = []
        for filename in filenames:
            with open(filename, 'r', encoding='utf-8') as file:
                lines.extend(file.readlines())
        return [line.strip() for line in lines]
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


# Функция для запуска игры
def start_game(screen, game_music=None):
    global continue_rect, back_rect
    pygame.mouse.set_visible(False)  # Скрываем стандартный курсор
    custom_cursor = pygame.image.load("Материал/курсор 2 (1).png")  # Загружаем кастомный курсор
    custom_cursor_rect = custom_cursor.get_rect(center=(0, 0))  # Устанавливаем центр курсора
    font = pygame.font.Font("LeoHand.ttf", 64)  # Устанавливаем шрифт LeoHand.ttf
    text_font = pygame.font.Font("LeoHand.ttf", 50)  # Шрифт для текста из файла
    input_font = pygame.font.Font("LeoHand.ttf", 48)  # Шрифт для текста ввода
    error_font = pygame.font.Font("LeoHand.ttf", 38)  # Шрифт для текста ошибки
    timer_font = pygame.font.Font("LeoHand.ttf", 50)  # Шрифт для таймера
    back_image = pygame.image.load("Материал/игра.jpg").convert()  # Загружаем фоновое изображение
    back_image = pygame.transform.scale(back_image, screen.get_size())  # Масштабируем фон
    running = True
    show_menu = False  # Флаг для отображения меню

    # Загружаем все строки из файлов и перемешиваем их
    all_lines = load_random_lines("Материал/Текст.txt", "Материал/сл.txt")
    random.shuffle(all_lines)  # Перемешиваем строки
    lines_iter = iter(all_lines)  # Создаем итератор для строк

    # Получаем первую случайную строку
    random_text = next(lines_iter, None)
    user_input = ""  # Переменная для хранения пользовательского ввода
    is_error = False  # Флаг для отображения ошибки
    texts_completed = 0  # Счётчик завершённых текстов
    total_texts = len(all_lines)  # Общее количество текстов для ввода

    # Устанавливаем начальное время
    start_time = pygame.time.get_ticks()
    timer_duration = 120 * 1000  # 60 секунд в миллисекундах

    while running:
        screen.blit(back_image, (0, 0))  # Отрисовываем фон
        mouse_pos = pygame.mouse.get_pos()  # Получаем позицию мыши
        custom_cursor_rect.center = mouse_pos  # Обновляем позицию курсора

        # Рассчитываем оставшееся время
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, timer_duration - elapsed_time)
        timer_seconds = remaining_time // 1000  # Переводим в секунды
        timer_text = f"{timer_seconds // 60}:{timer_seconds % 60:02d}"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Включение меню нажатием ESC
                    show_menu = not show_menu

                elif event.key == pygame.K_BACKSPACE:  # Удалить последний символ
                    user_input = user_input[:-1]

                elif event.key == pygame.K_RETURN:  # Конечный ввод (enter)
                    if user_input.strip() == random_text.strip():
                        print("Текст введен правильно!")
                        is_error = False  # Ошибки нет, если текст правильный
                        texts_completed += 1  # Увеличить счетчик завершенных текстов
                        random_text = next(lines_iter, None)  # Получаем следующую строку
                        if random_text is None:  # Если больше нет строк
                            running = False  # Завершаем игру
                    else:
                        print("Ошибка в введенном тексте.")
                        is_error = True  # Устанавлеваем флаг ошибки

                    user_input = ""  # Очщаем строку ввода

                elif event.key == pygame.K_SPACE:
                    user_input += "  "  # Ставим два пробела

                else:
                    user_input += event.unicode  # Добавляем символ для ввода

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_menu:
                    if event.button == 1:  # Левая кнопка мыши
                        if continue_rect.collidepoint(event.pos):  # Нажимаем "Продолжить"
                            show_menu = False  # Закрыть меню
                        elif back_rect.collidepoint(event.pos):  # Нажимаем "Назад"
                            return  # Выход в главное меню

        # Проверяем, истек ли таймер
        if remaining_time <= 0:
            running = False  # Заканчиваем игру, если таймер истек

        # Отображаем случайную строку из файлов
        text_surface = text_font.render(random_text, True, (212, 163, 115))  # Отрисовываем текст
        # Центрируем текст чуть выше
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 205))
        screen.blit(text_surface, text_rect.topleft)  # Позиция для отображения текста

        # Отображаем текстовый ввод в центре экрана
        input_surface = input_font.render(user_input, True, (204, 213, 174))  # Отображаем введённый текст
        # Центрируем текст
        input_rect = input_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - (-10)))
        screen.blit(input_surface, input_rect)

        # Выводим сообщение о ошибке, если это необходимо
        if is_error:
            error_surface = error_font.render("Ошибка!", True, (223, 126, 104))  # Отображаем текст ошибки
            # Центрируем текст ошибки
            error_rect = error_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - (- 94)))
            screen.blit(error_surface, error_rect.topleft)

        # Отображаем таймер в правом верхнем углу
        timer_surface = timer_font.render(timer_text, True, (212, 139, 115))  # Отображаем текст таймера
        timer_rect = timer_surface.get_rect(topright=(screen.get_width() - 50, 46))  # Позиция таймера
        screen.blit(timer_surface, timer_rect)

        # Открываем меню только при необходимости
        if show_menu:
            menu_rect = pygame.Rect(200, 190, 400, 200)  # Создаем прямоугольник для меню
            pygame.draw.rect(screen, (254, 250, 224), menu_rect)  # Рисуем меню

            # Настройка текста
            continue_rect = pygame.Rect(250, 200, 300, 64)  # Прямоугольник "Продолжить"
            back_rect = pygame.Rect(250, 300, 300, 64)  # Прямоугольник "Назад"
            continue_text_color = (204, 213, 174)  # Исходный цвет текста "Продолжить"
            back_text_color = (204, 213, 174)  # Исходный цвет текста "Назад"

            # Изменяем цвет текста при наведении
            if continue_rect.collidepoint(mouse_pos):
                continue_text_color = (212, 163, 115)  # Цвет текста при наведении на "Продолжить"
            if back_rect.collidepoint(mouse_pos):
                back_text_color = (212, 163, 115)  # Цвет текста при наведении на "Назад"

            continue_text = font.render("Продолжить", True, continue_text_color)  # Текст "Продолжить"
            back_text = font.render("Назад", True, back_text_color)  # Текст "Назад"

            screen.blit(continue_text, continue_rect)  # Отрисовываем текст "Продолжить"
            screen.blit(back_text, back_rect)  # Отрисовываем текст "Назад"

        screen.blit(custom_cursor, custom_cursor_rect)  # Отрисовываем кастомный курсор
        pygame.display.flip()  # Обновляем экран

    # Игра окончена, выводим сообщение игроку
    result_action = display_result(screen, back_image, font, texts_completed, total_texts)

    # Проверяем результат действия и соответствующим образом действуем
    if result_action == "restart":
        start_game(screen)  # Запускаем игру заново
    elif result_action == "menu":
        return  # Переход в главное меню


# Пример инициализации и запуска игры:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Задаем размер экрана
    pygame.display.set_caption("Таймер и Ввод Текста")  # Заголовок окна
    start_game(screen)
