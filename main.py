from pygame import *
import pygame
import player
import monsters
import blocks
import sys

WIN_WIDTH = 800 #Ширина окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

timer = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Moy Super Mario")  # Пишем в шапку

def main():
    bg = Background('data/background.jpg', [0, 0])
    hero = player.Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = up = False  # по умолчанию — стоим

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)

    animatedEntities = pygame.sprite.Group()  # все анимированные объекты, за исключением героя
    monster = pygame.sprite.Group()  # Все передвигающиеся объекты

    level = [
        "----------------------------------",
        "-                                -",
        "-                       *        -",
        "-                                -",
        "-            --                  -",
        "-                           --   -",
        "-----                            -",
        "-                                -",
        "-                  ----     --- -",
        "-P -                             -",
        "----                             -",
        "-            ----                -",
        "-                            --- -",
        "-                                -",
        "-                  --            -",
        "-      *-*                       -",
        "-                                -",
        "-   -------                      -",
        "-             --                 -",
        "-                                -",
        "-                 --             -",
        "-        --**                    -",
        "-                                -",
        "----------------------------------"]

    timer = pygame.time.Clock()

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = blocks.Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            if col == "*":
                bd = blocks.BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)

            if col == "P":
                pr = blocks.Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0

    tp = blocks.BlockTeleport(128, 512, 800, 64)
    entities.add(tp)
    platforms.append(tp)
    animatedEntities.add(tp)
    running = True

    mn = monsters.Monster(190, 230, 2, 3, 150, 15)
    entities.add(mn)
    platforms.append(mn)
    monster.add(mn)

    while running:  # Основной цикл программы
        timer.tick(30)
        screen.blit(bg.image, bg.rect)
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
        camera.update(hero)  # центризируем камеру относительно персонажа
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # обновление и вывод всех изменений на экран
        pygame.display.flip()
        animatedEntities.update()
        monster.update(platforms)  # передвигаем всех монстров



class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2
    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

if __name__ == "__main__":
    main()