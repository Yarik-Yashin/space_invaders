import os
import pygame
import sys
import random


def load_image(name, size, colorkey=None):
    fullname = os.path.join('img', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, size)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Object:
    def render(self, img):
        pass


class Player:
    def __init__(self):
        self.lives = 4
        self.score = 0
        self.position = 50

    def move(self, left: bool):
        if left:
            self.position = self.position - 5
        else:
            self.position = self.position + 5
        return self.position


class Bullet:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def check(self, enemy_x: int, enemy_y: int):
        if self.x == enemy_x and self.y == enemy_y:
            return 1
        else:
            return 0

    def move(self, down: bool):
        self.y = self.y - 10 if down else self.y + 10


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy.png", (30, 30))
    image2 = load_image("enemy1.png", (30, 30))
    images = [image, image2]

    def __init__(self, group, x, y):

        super().__init__(group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.o = 0
        self.k = 200

    def update(self, *args):

        if self.o < self.k:
            n = 2
            self.k = 200

        else:
            n = -2
            self.k = 0
        if n > 0:
            self.image = Enemy.image2
        else:
            self.image = Enemy.image
        self.rect = self.rect.move(n, 0)
        self.o += n
        if pygame.sprite.spritecollideany(self, hero_bullets_sprites):
            self.kill()
            pygame.sprite.spritecollideany(self, hero_bullets_sprites).kill()


class Hero(pygame.sprite.Sprite):
    image = load_image("hero.png", (50, 50))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, n):
        self.rect = self.rect.move(n, 0)


class HeroBullet(pygame.sprite.Sprite):
    image = load_image("bullet1.png", (50, 50))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = HeroBullet.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        self.rect = self.rect.move(0, -20)
        '''if pygame.sprite.spritecollideany(self, enemy_sprites):
            self.kill()'''


class Building(pygame.sprite.Sprite):
    image = load_image("building.png", (50, 50))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Building.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


if __name__ == '__main__':

    W = 600
    H = 600

    screen = pygame.display.set_mode((W, H))
    pygame.display.update()
    fps = 24
    clock = pygame.time.Clock()
    hero_bullets_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()
    hero = Hero(hero_sprite, 300, 520)
    buildings_sprites = pygame.sprite.Group()
    for i in range(4):
        Building(buildings_sprites, 150 * i + 20, 460)
    for i in range(10):
        for j in range(6):
            Enemy(enemy_sprites, 41 * i, 41 * j)
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            keys = pygame.key.get_pressed()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_RIGHT:
                    hero_sprite.update(n=10)
                if i.key == pygame.K_LEFT:
                    hero_sprite.update(n=-10)
                if i.key == pygame.K_SPACE:
                    HeroBullet(hero_bullets_sprites, hero.rect.x, hero.rect.y)
        screen.fill((0, 0, 0))
        hero_sprite.draw(screen)
        hero_bullets_sprites.draw(screen)
        hero_bullets_sprites.update()
        enemy_sprites.draw(screen)
        enemy_sprites.update()
        buildings_sprites.draw(screen)
        pygame.display.update()
        clock.tick(fps)
