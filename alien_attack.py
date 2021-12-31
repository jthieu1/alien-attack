# Alien Attack the Simple Arcade Game
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


def draw_bg():
    screen.fill(black_color)
    pygame.display.flip()


run = True
while run:
    clock.tick(fps)
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
