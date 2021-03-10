
import pygame
import glob

# initialize pygame
pygame.init()

# screen size
screen = pygame.display.set_mode((800, 600))

# game title
pygame.display.set_caption("Galaxy Shooter")


class Spaceship:

    def __init__(self):
        self.body = pygame.image.load('spaceship.png')
        self.body  = pygame.transform.scale(self.body, (50, 50))
        self.positionX = 400
        self.positionY = 500

    def addToScreen(self):
        screen.blit(self.body, (self.positionX, self.positionY))

    def moveLeft(self, step = 10):
        self.positionX =  self.positionX - step

    def moveRight(self, step = 10):
        self.positionX =  self.positionX + step



running = True
spaceship = Spaceship()

while running:

    screen.fill((28, 114, 189))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        pressed_keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_LEFT:
                print("left down")
                spaceship.moveLeft()

            if event.key == pygame.K_RIGHT:
                print("right down")
                spaceship.moveRight()

    # add spcaeship on the screen
    spaceship.addToScreen()
    pygame.display.update()

        