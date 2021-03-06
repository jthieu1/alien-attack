# Alien Attack - the Simple Arcade Game
# By Jenny and Dan
import random

import pygame
import pygame.sprite
import pygame.time
from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

music = pygame.mixer.Sound('sound/bgm.wav')
music.set_volume(0.5)
music.play(-1, 0, 0)

# FPS
clock = pygame.time.Clock()
fps = 60

# screen display settings
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Alien Attack')

# fonts
font_35 = pygame.font.SysFont('Consolas', 35)
font_38 = pygame.font.SysFont('Consolas', 38)
font_40 = pygame.font.SysFont('Consolas', 40)


# load sounds
expl_fx = pygame.mixer.Sound("sound/explosion.wav")
expl_fx.set_volume(0.30)

expl2_fx = pygame.mixer.Sound("sound/explosion.wav")
expl2_fx.set_volume(0.10)

bullet_fx = pygame.mixer.Sound("sound/bullet.wav")
bullet_fx.set_volume(0.30)

rows = 5
columns = 5
alien_cooldown = 1000  # cooldown of aliens shooting
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0

# background
black_color = (0, 0, 0)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
white_color = (255, 255, 255)


def draw_bg():
    screen.fill(black_color)


def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    screen.blit(image, (x, y))


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.hp_start = hp
        self.hp_left = hp
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        global game_over
        speed = 8  # Sets the movement speed
        cooldown = 500  # Sets the cooldown variable between each bullet that can be fired, in milliseconds

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        # current time
        curr_time = pygame.time.get_ticks()

        # checks for shooting, creates bullet everytime space is pressed
        if key[pygame.K_SPACE] and curr_time - self.last_shot > cooldown:
            bullet_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = curr_time

        # updates the mask, so this ignores the transparent part of the spaceship
        self.mask = pygame.mask.from_surface(self.image)

        # draws health bar
        pygame.draw.rect(screen, red_color, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.hp_left > 0:
            pygame.draw.rect(screen, green_color, (self.rect.x, (self.rect.bottom + 10),
                                                   int(self.rect.width * (self.hp_left / self.hp_start)),
                                                   15))
        elif self.hp_left <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        # if bottom of the bullet has gone off the screen
        if self.rect.bottom < 0:
            self.kill()

        if pygame.sprite.spritecollide(self, aliens_group, True):
            self.kill()
            expl_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)  # for mid-sized explosions
            explosion_group.add(explosion)


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/alien" + str(random.randint(1, 4)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            # Fourth parameter ensures proper collision with spaceship
            self.kill()
            expl2_fx.play()
            # This will reduce spaceship's health
            spaceship.hp_left -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)  # for tiny-sized explosions
            explosion_group.add(explosion)


# explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 64):
            exp_img = pygame.image.load(f"images/PNG/frame{num}.png")
            if size == 1:
                exp_img = pygame.transform.scale(exp_img, (20, 20))
            if size == 2:
                exp_img = pygame.transform.scale(exp_img, (40, 40))
            if size == 3:
                # large size explosion for ship
                exp_img = pygame.transform.scale(exp_img, (160, 160))
            self.images.append(exp_img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explo_speed = 3
        # update explosion animation
        self.counter += 1
        if self.counter == explo_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # complete animation, delete explosion
        if self.index >= len(self.images) > 1 and self.counter >= explo_speed:
            self.kill()


# create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
alien_bullets_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def spawn_aliens():
    for row in range(rows):
        for item in range(rows):
            aliens = Aliens(100 + item * 100, 100 + row * 70)
            aliens_group.add(aliens)


spawn_aliens()

# create the player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)
run = True
while run:
    clock.tick(fps)
    draw_bg()

    if countdown > 0:
        draw_text('GAME START:', font_40, white_color, int(screen_width / 2 - 160), int(screen_height / 2 - 275))
        draw_text(str(countdown), font_35, white_color, int(screen_width / 2 + 110), int(screen_height / 2 - 271))
        cd_timer = pygame.time.get_ticks()
        if cd_timer - last_count > 1000:
            countdown -= 1
            last_count = cd_timer

    if countdown == 0:
        time_now = pygame.time.get_ticks()
        # alien shooting
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullets_group) < 5 and len(aliens_group) > 0:
            attacking_alien = random.choice(aliens_group.sprites())
            alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullets_group.add(alien_bullet)
            last_alien_shot = time_now

        # print(spaceship.rect.x)

        # if all aliens have been killed
        if len(aliens_group) == 0:
            game_over = 1

        if game_over == 0:
            game_over = spaceship.update()

            # update sprite groups
            bullet_group.update()
            aliens_group.update()
            alien_bullets_group.update()
        else:
            if game_over == -1:
                draw_text('GAME OVER!', font_40, white_color, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
            if game_over == 1:
                draw_text('YOU WIN!', font_40, white_color, int(screen_width / 2 - 100), int(screen_height / 2 + 50))

    explosion_group.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    aliens_group.draw(screen)
    alien_bullets_group.draw(screen)
    explosion_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
