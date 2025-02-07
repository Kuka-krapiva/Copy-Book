import pygame
import sys
from . import настройки  # Предполагая, что файл "настройки.py" находится в той же директории

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры экрана
screen_width = 1050
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Главное меню")

# Загружаем фоновое изображение
background = pygame.image.load("Материал/a889004c62b06dfbf3351f257b9799db.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Определяем цвета
WHITE = (246, 246, 246)
font_color = (135, 133, 162)
hover_color = (255, 199, 199)  # Цвет при наведении
font = pygame.font.Font(None, 64)

# Загружаем шрифты
font = pygame.font.Font("LeoHand.ttf", 64)
font_title = pygame.font.Font("LeoHand.ttf", 100)


def draw_button(text, pos, is_hover):
    color = hover_color if is_hover else font_color
    label = font.render(text, True, color)
    label_rect = label.get_rect(center=pos)
    screen.blit(label, label_rect)


def main_menu():
    # Основной цикл
    while True:
        screen.blit(background, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Проверяем, наведён ли курсор на кнопки
        start_hover = 350 <= mouse_x <= 850 and 300 - 53 <= mouse_y <= 300 + 32
        settings_hover = 350 <= mouse_x <= 850 and 400 - 53 <= mouse_y <= 400 + 32
        exit_hover = 350 <= mouse_x <= 850 and 500 - 53 <= mouse_y <= 500 + 32

        # Отображаем кнопки с учетом наведения
        draw_button("Начать игру", (screen_width // 1.4, 250), start_hover)
        draw_button("Настройки", (screen_width // 1.4, 350), settings_hover)
        draw_button("Выход", (screen_width // 1.4, 450), exit_hover)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                if start_hover:
                    print("Кнопка 'Начать игру' нажата")
                    # Логика для начала игры
                elif settings_hover:
                    print("Кнопка 'Настройки' нажата")
                    настройки.settings_menu(screen)  # Открытие меню настроек
                elif exit_hover:
                    pygame.quit()
                    sys.exit()  # Закрытие игры

        pygame.display.flip()  # Обновляем экран
