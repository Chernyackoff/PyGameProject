from pygame import *
import pygame
import player
import blocks
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
    left = right= up = False  # по умолчанию — стоим

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)
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
    timer = pygame.time.Clock()

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = blocks.Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0

    running = True
    while running:  # Основной цикл программы
        timer.tick(30)
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == KEYDOWN and event.key == K_UP:
                up = True

            if event.type == KEYUP and event.key == K_UP:
                up = False
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
        hero.update(left, right, up, platforms)  # передвижение
        entities.draw(screen)  # отображение всего
        pygame.display.update()  # обновление и вывод всех изменений на экран
        pygame.display.flip()


if __name__ == "__main__":
    main()