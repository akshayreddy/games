import pygame, random

from bullet import SpaceshipBullet

class Star:
    stepSize = 0.1

    def __init__(self, screen, gameScreenX, gameScreenY):
        self.screen = screen
        self.bodyX = 10
        self.bodyY = 10
        self.body = pygame.image.load('../assets/star.svg')
        self.body = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.positionX = random.randint(0, gameScreenX)
        self.positionY = random.randint(0, gameScreenY)

    def addToScreen(self):
        self.screen.blit(self.body, (self.positionX, self.positionY))

    def move(self):
        self.positionY = self.positionY + self.stepSize
        self.addToScreen()
        pass