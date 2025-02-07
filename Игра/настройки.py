import pygame
import sys
import json
import os

SETTINGS_FILE = 'settings.json'


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {'volume': 1.0}  # значение по умолчанию


def save_settings(volume):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as file:
        json.dump({'volume': volume}, file)


def set_volume(volume):
    save_settings(volume)
    pygame.mixer.music.set_volume(volume)


def settings_menu(screen):
    pygame.mouse.set_visible(False)  # Скрыть стандартный курсор
    custom_cursor = pygame.image.load("Материал/курсор 2 (1).png")  # Загрузка пользовательского курсора
    custom_cursor_rect = custom_cursor.get_rect(center=(0, 0))  # Прямоугольник для пользовательского курсора
    font = pygame.font.Font("LeoHand.ttf", 64)  # Используем конкретный шрифт
    font_n = pygame.font.Font("LeoHand.ttf", 69)
    font_m = pygame.font.Font("LeoHand.ttf", 55)
    back_image = pygame.image.load("Материал/настройки.jpg").convert()  # Загрузка фонового изображения
    back_image = pygame.transform.scale(back_image, screen.get_size())  # Масштаб под размер экрана
    running = True

    back_normal_color = (212, 163, 115)
    back_hover_color = (204, 213, 174)

    # Загружаем предыдущие настройки громкости
    settings = load_settings()
    volume_level = settings.get('volume', 1.0)  # Начальный уровень громкости из настроек

    while running:
        screen.blit(back_image, (0, 0))
        label = font.render("Настройки", True, (212, 163, 115))
        screen.blit(label, (screen.get_width() // 2 - label.get_width() // 2, 30))

        back_button = font.render("Назад", True, back_normal_color)
        back_button_rect = back_button.get_rect(center=(screen.get_width() // 2, 620))
        screen.blit(back_button, back_button_rect)

        # Кнопки для изменения громкости
        increase_volume_button = font_n.render("+", True, back_normal_color)
        decrease_volume_button = font_n.render("-", True, back_normal_color)

        increase_volume_button_rect = increase_volume_button.get_rect(center=(screen.get_width() // 2, 298))
        decrease_volume_button_rect = decrease_volume_button.get_rect(center=(screen.get_width() // 2, 459))

        screen.blit(increase_volume_button, increase_volume_button_rect)
        screen.blit(decrease_volume_button, decrease_volume_button_rect)

        # Отображаем текущий уровень громкости
        volume_text = font_m.render(f"Громкость: {int(volume_level * 100)}%", True, back_normal_color)
        screen.blit(volume_text, (screen.get_width() // 2 - volume_text.get_width() // 2, 300))

        # Графический индикатор громкости
        volume_bar_width = 300
        volume_bar_height = 30
        volume_bar_x = (screen.get_width() - volume_bar_width) // 2
        volume_bar_y = 400

        # Рисуем контейнер для индикатора громкости
        pygame.draw.rect(screen, (212, 163, 115), (volume_bar_x, volume_bar_y, volume_bar_width, volume_bar_height))
        # Рисуем заполненную часть индикатора громкости
        pygame.draw.rect(screen, (204, 213, 174),
                         (volume_bar_x, volume_bar_y, volume_bar_width * volume_level, volume_bar_height))

        mouse_pos = pygame.mouse.get_pos()
        custom_cursor_rect.center = mouse_pos  # Установить позицию пользовательского курсора

        # Проверяем, наведена ли мышь на кнопки
        if back_button_rect.collidepoint(mouse_pos):
            back_button = font.render("Назад", True, back_hover_color)
        else:
            back_button = font.render("Назад", True, back_normal_color)

        if increase_volume_button_rect.collidepoint(mouse_pos):
            increase_volume_button = font.render("Увеличить громкость", True, back_hover_color)
        if decrease_volume_button_rect.collidepoint(mouse_pos):
            decrease_volume_button = font.render("Уменьшить громкость", True, back_hover_color)

        screen.blit(back_button, back_button_rect)  # Обновление цвета кнопки
        screen.blit(custom_cursor, custom_cursor_rect)  # Отображение пользовательского курсора

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                if back_button_rect.collidepoint(event.pos):
                    running = False
                elif increase_volume_button_rect.collidepoint(event.pos):
                    volume_level = min(volume_level + 0.1, 1.0)  # Увеличиваем громкость
                    pygame.mixer.music.set_volume(volume_level)  # Устанавливаем громкость музыки
                    save_settings(volume_level)  # Сохраняем настройки
                elif decrease_volume_button_rect.collidepoint(event.pos):
                    volume_level = max(volume_level - 0.1, 0.0)  # Уменьшаем громкость
                    pygame.mixer.music.set_volume(volume_level)  # Устанавливаем громкость музыки
                    save_settings(volume_level)  # Сохраняем настройки

        pygame.display.flip()
