import pygame
import sys
import random
from конец import display_result
from настройки import load_settings, save_settings  # Импортируем функции для работы с настройками
from threading import Timer


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
    pygame.mouse.set_visible(False)

    # Загрузка настроек
    settings = load_settings()
    volume = settings.get('volume', 1.0)  # Получаем громкость из настроек
    pygame.mixer.music.set_volume(volume)  # Устанавливаем громкость музыки

    custom_cursor = pygame.image.load("Материал/курсор 2 (1).png")
    custom_cursor_rect = custom_cursor.get_rect(center=(0, 0))
    font = pygame.font.Font("LeoHand.ttf", 64)
    text_font = pygame.font.Font("LeoHand.ttf", 50)
    input_font = pygame.font.Font("LeoHand.ttf", 48)
    error_font = pygame.font.Font("LeoHand.ttf", 38)
    timer_font = pygame.font.Font("LeoHand.ttf", 50)
    back_image = pygame.image.load("Материал/игра.jpg").convert()
    back_image = pygame.transform.scale(back_image, screen.get_size())
    running = True
    show_menu = False

    # Загрузка и перемешивание строк текста
    all_lines = load_random_lines("Материал/Текст.txt", "Материал/сл.txt")
    random.shuffle(all_lines)
    lines_iter = iter(all_lines)

    # Инициализация переменных для текста и ввода пользователя
    random_text = next(lines_iter, None)
    user_input = ""
    is_error = False
    texts_completed = 0
    total_texts = len(all_lines)

    # Настройка таймера
    timer_duration = 91  # Полторы минуты
    remaining_time = timer_duration
    timer = None

    # Функция обновления таймера
    def update_timer():
        nonlocal remaining_time, timer
        if remaining_time > 0:
            remaining_time -= 1
            timer = Timer(1, update_timer)
            timer.start()

    # Запуск таймера
    update_timer()

    while running:
        # Отрисовка фона и курсора
        screen.blit(back_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        custom_cursor_rect.center = mouse_pos

        # Форматирование текста таймера
        timer_text = f"{remaining_time // 60}:{remaining_time % 60:02d}"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Завершение игры и отмена таймера
                if timer:
                    timer.cancel()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Открытие/закрытие меню
                    show_menu = not show_menu
                    if show_menu:
                        if timer:
                            timer.cancel()  # Остановка таймера
                    else:
                        update_timer()  # Продолжение таймера

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]

                elif event.key == pygame.K_RETURN:
                    if user_input.strip() == random_text.strip():
                        is_error = False
                        texts_completed += 1
                        random_text = next(lines_iter, None)
                        if random_text is None:
                            running = False
                    else:
                        is_error = True

                    user_input = ""

                elif event.key == pygame.K_SPACE:
                    user_input += "  "

                elif event.key == pygame.K_UP:
                    # Увеличение громкости
                    volume = min(volume + 0.1, 1.0)  # Максимальная громкость — 1.0
                    pygame.mixer.music.set_volume(volume)
                    save_settings(volume)  # Сохранение новой громкости

                elif event.key == pygame.K_DOWN:
                    # Уменьшение громкости
                    volume = max(volume - 0.1, 0.0)  # Минимальная громкость — 0.0
                    pygame.mixer.music.set_volume(volume)
                    save_settings(volume)  # Сохранение новой громкости

                else:
                    user_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_menu:
                    if event.button == 1:
                        if continue_rect.collidepoint(event.pos):
                            show_menu = False
                            update_timer()  # Продолжение таймера
                        elif back_rect.collidepoint(event.pos):
                            if timer:
                                timer.cancel()
                            return

        if remaining_time <= 0:
            running = False

        # Отрисовка текста и ввода
        text_surface = text_font.render(random_text, True, (212, 163, 115))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 205))
        screen.blit(text_surface, text_rect.topleft)

        input_surface = input_font.render(user_input, True, (204, 213, 174))
        input_rect = input_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - (-10)))
        screen.blit(input_surface, input_rect)

        # Отображение ошибки
        if is_error:
            error_surface = error_font.render("Ошибка!", True, (223, 126, 104))
            error_rect = error_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - (-94)))
            screen.blit(error_surface, error_rect.topleft)

        # Отрисовка таймера
        timer_surface = timer_font.render(timer_text, True, (212, 139, 115))
        timer_rect = timer_surface.get_rect(topright=(screen.get_width() - 50, 46))
        screen.blit(timer_surface, timer_rect)

        if show_menu:
            # Отрисовка меню
            menu_rect = pygame.Rect(200, 190, 400, 200)
            pygame.draw.rect(screen, (254, 250, 224), menu_rect)

            continue_rect = pygame.Rect(250, 200, 300, 64)
            back_rect = pygame.Rect(250, 300, 300, 64)
            continue_text_color = (204, 213, 174)
            back_text_color = (204, 213, 174)

            if continue_rect.collidepoint(mouse_pos):
                continue_text_color = (212, 163, 115)
            if back_rect.collidepoint(mouse_pos):
                back_text_color = (212, 163, 115)

            continue_text = font.render("Продолжить", True, continue_text_color)
            back_text = font.render("Назад", True, back_text_color)

            screen.blit(continue_text, continue_rect)
            screen.blit(back_text, back_rect)

        screen.blit(custom_cursor, custom_cursor_rect)
        pygame.display.flip()

    # Отображение результата и выбор действия
    result_action = display_result(screen, back_image, font, texts_completed, total_texts)

    if result_action == "restart":
        start_game(screen)
    elif result_action == "menu":
        return


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Таймер и Ввод Текста")
    start_game(screen)
