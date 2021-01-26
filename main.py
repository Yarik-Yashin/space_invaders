import os
import pygame
import sys
import random
import time


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Выигрывайте",
                  "Если проиграите, случится проигрыш"]

    fon = pygame.transform.scale(load_image('fon.png', (W, H)), (W, H))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    a = 1
    while a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = 0

            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)


def end_screen():
    intro_text = ["ХАА ХАХАХАХАХ ВЫ ПРОИГРАЛИ !!!!!", "",
                  "ВЫ ПРОИГРАЛИ ХАХАХАХАХ",
                  "В СЛЕДУЮЩИЙ РАЗ НЕ ПРОИГРЫВАЙТЕ ХАХАХАХАХАХ",
                  "Если проиграите еще раз, случится очередной проигрыш"]

    fon = pygame.transform.scale(load_image('fon.png', (W, H)), (W, H))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    pygame.mixer.music.load('audio/end.mp3')
    pygame.mixer.music.play()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    a = 1
    while a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = 0
        pygame.display.flip()
        clock.tick(60)


def new_game(slozn):
    global sl
    hero = Hero(hero_sprite, 300, 520)
    for i in range(4):
        Building(buildings_sprites, 150 * i + 20, 460)
    for i in range(6 * int(slozn / 2)):
        for j in range(6):
            Enemy(enemy_sprites, 41 * i, 41 * j)
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
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
        bang_sprites.draw(screen)
        bang_sprites.update()
        hero_sprite.update(n=0)
        font = pygame.font.Font(None, 25)
        text = font.render(f"Your lives:{hero.health - 1}", True, (100, 255, 100))
        text1 = font.render(f"Hard:{slozn - 1}", True, (100, 255, 100))
        screen.blit(text, (10, 520))
        screen.blit(text1, (10, 560))
        if len(enemy_sprites) == 0:
            return
        if len(buildings_sprites) == 0 or hero.health <= 0:
            sl = 0 - sl
            return
        for i in enemy_sprites:
            if i.rect.y > 600:
                sl = 0 - sl
                return
        pygame.display.update()
        fps = 720 / (len(enemy_sprites) + 1)

        clock.tick(fps)


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
            n = 1
            self.k = 200

        else:
            n = -1
            self.k = 0
        if n > 0:
            self.image = Enemy.image2
        else:
            self.image = Enemy.image
        if self.o == 0 or self.o == 200:
            self.rect = self.rect.move(n, 30)
        else:
            self.rect = self.rect.move(n, 0)
        self.o += n
        if pygame.sprite.spritecollideany(self, hero_bullets_sprites):
            self.kill()
            pygame.mixer.music.load('audio/pau.mp3')
            pygame.mixer.music.play()
            pygame.sprite.spritecollideany(self, hero_bullets_sprites).kill()
            Bang(bang_sprites, self.rect.x, self.rect.y)
        if random.randint(0, 2400 / sl) == 5:
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
    image = load_image("bullet1.png", (5, 20))

    def __init__(self, group, x, y):
        super().__init__(group)
        pygame.mixer.music.load('audio/piu.mp3')
        pygame.mixer.music.play()
        self.image = HeroBullet.image
        self.rect = self.image.get_rect()
        self.rect.x = x + 20
        self.rect.y = y

    def update(self, *args):
        self.rect = self.rect.move(0, -20)
        if self.rect.y < 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, enemy_bullets_sprites):
            self.kill()
            pygame.sprite.spritecollideany(self, enemy_bullets_sprites).kill()


class Bang(pygame.sprite.Sprite):
    image = load_image("babah.png", (30, 30))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Bang.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.n = 0

    def update(self, *args):
        self.n += 1
        if self.n == 10:
            self.kill()


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
        if pygame.sprite.spritecollideany(self, enemy_sprites):
            pygame.mixer.music.load('audio/babah.mp3')
            pygame.mixer.music.play()
            pygame.sprite.spritecollideany(self, enemy_sprites).kill()
            self.kill()
        if pygame.sprite.spritecollideany(self, hero_bullets_sprites or enemy_bullets_sprites):
            self.health += 1
            if self.health == 6:
                self.kill()
                pygame.mixer.music.load('audio/babah.mp3')
                pygame.mixer.music.play()
            else:
                pygame.sprite.spritecollideany(self, hero_bullets_sprites or enemy_bullets_sprites).kill()
                self.image = load_image("building" + str(self.health) + ".png", (50, 50))
                pygame.mixer.music.load('audio/babah.mp3')
                pygame.mixer.music.play()


if __name__ == '__main__':
    W = 600
    H = 600
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((W, H))

    clock = pygame.time.Clock()
    start_screen()
    hero_bullets_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    bang_sprites = pygame.sprite.Group()
    enemy_bullets_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()

    buildings_sprites = pygame.sprite.Group()

    sl = 1
    while sl != 0:
        new_game(sl)
        sl += 1
        hero_bullets_sprites.empty()
        enemy_sprites.empty()
        bang_sprites.empty()
        enemy_bullets_sprites.empty()
        hero_sprite.empty()

        buildings_sprites.empty()
    end_screen()
