import pygame
import sys
import настройки
import игра

# Инициализация Pygame
pygame.init()

# Инициализация микшера для воспроизведения музыки
pygame.mixer.init()
pygame.mixer.music.load("Материал/Blue Skies.mp3")  # Загружаем музыку
pygame.mixer.music.set_volume(0.2)  # Устанавливаем громкость на 20%
pygame.mixer.music.play(-1)  # Воспроизводим музыку бесконечно (-1)

# Устанавливаем размеры экрана
screen_width = 800
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Copy-Book")

# Загружаем фоновое изображение
background = pygame.image.load("Материал/фонМЕНЮ.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Определяем цвета
WHITE = (255, 199, 199)
font_color = (135, 133, 162)
hover_color = (255, 199, 199)
info_color = (0, 0, 0)  # Цвет текста для окна с информацией

# Загружаем шрифты
font = pygame.font.Font("LeoHand.ttf", 64)
font_title = pygame.font.Font("LeoHand.ttf", 100)
font_info = pygame.font.Font("LeoHand.ttf", 24)

# Загрузка курсора
cursor_image = pygame.image.load("Материал/курсор 2 (1).png")
pygame.mouse.set_visible(False)  # Скрываем стандартный курсор

# Флаг для отображения окна информации
show_info = False
info_text = ""


# Функция для загрузки содержимого файла
def load_info():
    global info_text
    with open("Материал/О игре.txt", "r", encoding="utf-8") as f:
        info_text = f.read()


# Функция для отображения кнопок
def draw_button(text, pos, is_hover):
    color = hover_color if is_hover else font_color
    label = font.render(text, True, color)
    label_rect = label.get_rect(center=pos)
    screen.blit(label, label_rect)


# Функция для отображения окна информации
def draw_info_window():
    pygame.draw.rect(screen, WHITE, (100, 100, 600, 500))  # Прямоугольник для окна
    pygame.draw.rect(screen, font_color, (100, 100, 600, 500), 5)  # Контур окна

    # Отображение текста информации
    lines = info_text.split("\n")
    for i, line in enumerate(lines):
        label = font_info.render(line, True, info_color)
        screen.blit(label, (120, 130 + i * 40))  # Отображаем каждую строку


# Основной цикл
while True:
    screen.blit(background, (0, 0))  # Отображаем фон
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Получаем позицию мыши

    # Обработка кнопок
    start_hover = 275 <= mouse_x <= 525 and 350 - 43 <= mouse_y <= 350 + 32
    settings_hover = 275 <= mouse_x <= 520 and 450 - 43 <= mouse_y <= 450 + 32
    exit_hover = 325 <= mouse_x <= 477 and 550 - 43 <= mouse_y <= 550 + 32
    info_hover = (mouse_x - 50) ** 2 + (mouse_y - 650) ** 2 <= 25 ** 2  # Положение круговой кнопки

    # Отображение заголовка и кнопок
    title = font_title.render("Copy - Book", True, font_color)
    title_rect = title.get_rect(center=(screen_width // 2, 200))
    screen.blit(title, title_rect)
    draw_button("Начать игру", (screen_width // 2, 350), start_hover)
    draw_button("Настройки", (screen_width // 2, 450), settings_hover)
    draw_button("Выход", (screen_width // 2, 550), exit_hover)

    # Отображение кнопки "?"
    pygame.draw.circle(screen, font_color, (50, 650), 25)  # Кнопка
    info_text_surface = font.render("?", True, WHITE)  # Текст
    info_text_rect = info_text_surface.get_rect(center=(50, 650))
    screen.blit(info_text_surface, info_text_rect)

    # Отображаем курсор
    screen.blit(cursor_image, (mouse_x, mouse_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            if start_hover:
                print("Кнопка 'Начать игру' нажата")
                игра.start_game(screen)
                # Логика для начала игры

            elif settings_hover:
                print("Кнопка 'Настройки' нажата")
                настройки.settings_menu(screen)
                # Открытие меню настроек

            elif exit_hover:
                pygame.quit()
                sys.exit()  # Закрытие игры

            elif info_hover:
                print("Кнопка '?' нажата")
                load_info()  # Загружаем информацию
                show_info = not show_info  # Переключаем отображение окна

    # Если нужно, отображаем окно информации
    if show_info:
        draw_info_window()

    pygame.display.flip()  # Обновляем экран
