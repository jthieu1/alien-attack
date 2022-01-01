# Alien Attack - the Simple Arcade Game
# By Jenny and Dan

import pygame
import pygame.time
from pygame.locals import *

# FPS
clock = pygame.time.Clock()
fps = 60

# screen display settings
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Alien Attack')

# background
black_color = (0, 0, 0)
red_color = (255, 0, 0)
green_color = (0, 255, 0)


def draw_bg():
    screen.fill(black_color)


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
        speed = 8       # Sets the movement speed
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
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = curr_time

        # draws health bar
        pygame.draw.rect(screen, red_color, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.hp_left > 0:
            pygame.draw.rect(screen, green_color, (self.rect.x, (self.rect.bottom + 10),
                                                   int(self.rect.width * (self.hp_left / self.hp_start)),
                                                   15))


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load("images/[].png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        # if bottom of the bullet has gone off the screen
        if self.rect.bottom < 0:
            self.kill()


# create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


# create the player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

run = True
while run:
    clock.tick(fps)
    draw_bg()

    # print(spaceship.rect.x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update spaceship
    spaceship.update()

    # updating sprite groups (Spaceship not updated as group)
    bullet_group.update()

    # update sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)

    pygame.display.update()

pygame.quit()
