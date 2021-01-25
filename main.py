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
        if random.randint(0, 1200) == 5:
            EnemyBullet(enemy_bullets_sprites, self.rect.x, self.rect.y)


class Hero(pygame.sprite.Sprite):
    image = load_image("hero.png", (60, 60))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 4

    def update(self, *args, n):
        self.rect = self.rect.move(n, 0)
        if pygame.sprite.spritecollideany(self, enemy_bullets_sprites):
            self.health -= 1
            self.rect.x = 300
            self.rect.y = 520


class HeroBullet(pygame.sprite.Sprite):
    image = load_image("bullet1.png", (5, 25))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = HeroBullet.image
        self.rect = self.image.get_rect()
        self.rect.x = x + 25
        self.rect.y = y

    def update(self, *args):
        self.rect = self.rect.move(0, -20)


class EnemyBullet(HeroBullet):
    def update(self, *args):
        self.rect = self.rect.move(0, 20)


class Building(pygame.sprite.Sprite):
    image = load_image("building0.png", (50, 50))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Building.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 0

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, hero_bullets_sprites or enemy_bullets_sprites):
            self.health += 1
            if self.health == 6:
                self.kill()
            else:
                pygame.sprite.spritecollideany(self, hero_bullets_sprites or enemy_bullets_sprites).kill()
                self.image = load_image("building" + str(self.health) + ".png", (50, 50))


if __name__ == '__main__':

    W = 600
    H = 600
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.update()
    clock = pygame.time.Clock()
    hero_bullets_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    enemy_bullets_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()
    hero = Hero(hero_sprite, 300, 520)
    buildings_sprites = pygame.sprite.Group()
    for i in range(4):
        Building(buildings_sprites, 150 * i + 20, 460)
    for i in range(10):
        for j in range(6):
            Enemy(enemy_sprites, 41 * i, 41 * j)
    fps = 24
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
                if i.key == pygame.K_SPACE and len(hero_bullets_sprites) < 1:
                    HeroBullet(hero_bullets_sprites, hero.rect.x, hero.rect.y)
        screen.fill((0, 0, 0))
        hero_sprite.draw(screen)
        hero_bullets_sprites.draw(screen)
        hero_bullets_sprites.update()
        enemy_sprites.draw(screen)
        enemy_sprites.update()
        enemy_bullets_sprites.draw(screen)
        enemy_bullets_sprites.update()
        buildings_sprites.draw(screen)
        buildings_sprites.update()
        hero_sprite.update(n=0)
        font = pygame.font.Font(None, 25)
        text = font.render(f"Your lives:{hero.health - 1}", True, (100, 255, 100))

        screen.blit(text, (10, 520))
        pygame.display.update()
        fps = 1440 / len(enemy_sprites)

        clock.tick(fps)
