
import pygame

# initialize pygame
pygame.init()

# screen size
screen = pygame.display.set_mode((800, 800))

# game title
pygame.display.set_caption("Galaxy Shooter")


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False






        