import pygame
import sys

def display_result(screen, back_image, font, texts_completed, total_texts):
    custom_cursor = pygame.image.load("Материал/курсор 2 (1).png") # Загружаем кастомный курсор
    custom_cursor_rect = custom_cursor.get_rect(center=(0, 0)) # Устанавливаем центр курсора

    # Отображаем фоновое изображение
    screen.blit(back_image, (0, 0))

    # Определяем сообщение в зависимости от результатов
    if texts_completed == total_texts:
        result_message = "Молодец!"  # Если игрок успел ввести все тексты
    else:
        result_message = "Не получилось :( Попробуй ещё!"

    # Отображаем сообщение
    result_surface = font.render(result_message, True, (204, 213, 174))
    result_rect = result_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 206))
    screen.blit(result_surface, result_rect)

    # Создание текста для кнопок
    restart_text = font.render("Заново", True, (204, 213, 174))
    menu_text = font.render("В меню", True, (204, 213, 174))

    restart_text_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 12))
    menu_text_rect = menu_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 120))

    pygame.display.flip()  # Обновляем экран после отображения результата

    # Бесконечный цикл для отображения результата
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Закрытие окна
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if restart_text_rect.collidepoint(event.pos):  # Проверяем нажата ли кнопка "Заново"
                        return "restart"  # Возвращаем значение для запуска игры заново
                    elif menu_text_rect.collidepoint(event.pos):  # Проверяем нажата ли кнопка "В меню"
                        return "menu"  # Возвращаем значение для перехода в меню

        # Проверяем положение курсора для изменения цвета кнопок
        mouse_pos = pygame.mouse.get_pos()

        # Цвета для кнопок
        restart_color = (204, 213, 174)  # Исходный цвет текста для "Заново"
        menu_color = (204, 213, 174)  # Исходный цвет текста для "В меню"

        # Меняем цвет текста кнопок при наведении
        if restart_text_rect.collidepoint(mouse_pos):
            restart_color = (212, 163, 115)  # Цвет текста при наведении на "Заново"
        if menu_text_rect.collidepoint(mouse_pos):
            menu_color = (212, 163, 115)  # Цвет текста при наведении на "В меню"

        # Отображаем кнопки с изменённым цветом
        restart_text = font.render("Заново", True, restart_color)
        menu_text = font.render("В меню", True, menu_color)

        # Просто обновляем экран, чтобы отобразить результат и кнопки
        screen.blit(back_image, (0, 0))  # Отображаем фоновое изображение
        screen.blit(result_surface, result_rect)  # Отображаем текст результата
        screen.blit(restart_text, restart_text_rect)  # Отображаем текст на кнопке "Заново"
        screen.blit(menu_text, menu_text_rect)  # Отображаем текст на кнопке "В меню"

        # Обновляем позицию кастомного курсора и отрисовываем его
        custom_cursor_rect.center = mouse_pos  # Обновляем позицию курсора
        screen.blit(custom_cursor, custom_cursor_rect)  # Отрисовываем кастомный курсор

        pygame.display.flip()  # Обновляем экран
