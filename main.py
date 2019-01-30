from pygame import *
import pygame
import player
import sys

WIN_WIDTH = 800 #Ширина окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

timer = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Moy Super Mario")  # Пишем в шапку

def main():
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    bg.fill(Color(BACKGROUND_COLOR))
    hero = player.Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию — стоим

    level = [
        "-------------------------",
        "-                       -",
        "-                       -",
        "-                       -",
        "-            --         -",
        "-                       -",
        "--                      -",
        "-                       -",
        "-                   --- -",
        "-                       -",
        "-                       -",
        "-      ---              -",
        "-                       -",
        "-   -----------        --",
        "-                       -",
        "-                -      -",
        "-                   --  -",
        "-                       -",
        "-                       -",
        "-------------------------"]

    running = True
    while running:  # Основной цикл программы
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    # создаем блок, заливаем его цветом и рисеум его
                    pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf.fill(Color(PLATFORM_COLOR))
                    screen.blit(pf, (x, y))

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0
        hero.update(left, right)  # передвижение
        hero.draw(screen)  # отображение
        pygame.display.update()  # обновление и вывод всех изменений на экран
        pygame.display.flip()


if __name__ == "__main__":
    main()