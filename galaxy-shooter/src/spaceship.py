import pygame
from bullet import SpaceshipBullet

class Spaceship:
    stepSize = 0.8

    def __init__(self, screen, gameScreenX, gameScreenY):
        self.gameScreenX = gameScreenX
        self.gameScreenY = gameScreenY 
        self.screen = screen
        self.bodyX = 50
        self.bodyY = 50
        self.body = pygame.image.load('spaceship.png')
        self.body = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.spaceshipMovement = 'stopped'
        self.positionX = 400
        self.positionY = 500
        self.bullets = []
        self.score = 0

    def addToScreen(self):
        self.screen.blit(self.body, (self.positionX, self.positionY))

    def moveLeft(self):
        # boundary on the left
        if self.positionX - self.stepSize > 0:
            self.positionX =  self.positionX - self.stepSize

    def moveRight(self):
        # boundary on the right
        if self.positionX + self.stepSize < self.gameScreenX - self.bodyX:
            self.positionX =  self.positionX + self.stepSize

    # fire a bullet
    def fire(self):
        if len(self.bullets) == 0:
            pygame.mixer.Sound('Gun+Silencer.wav').play()
            bullet = SpaceshipBullet(self.screen, self.positionX, self.positionY)
            self.bullets.append(bullet)
        else:
            pygame.mixer.Sound('Gun+Reload.wav').play()

    def rotate(self):
        for i in range(8):
            self.body = pygame.transform.rotate(self.body, 90)
            self.body = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))