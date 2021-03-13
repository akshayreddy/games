import pygame, math
from datetime import datetime

class Bullet:
    stepSize = 1

    def __init__(self, screen, positionX, positionY):
        self.screen = screen
        self.bodyX = 25
        self.bodyY = 25
        self.body = pygame.image.load('../assets/bullet.png')
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.positionX = positionX
        self.positionY = positionY
    
    def addToScreen(self):
        self.screen.blit(self.body, (self.positionX, self.positionY))

class SpaceshipBullet(Bullet):
    # move towards the enemy
    def move(self):
        self.positionY = self.positionY - self.stepSize
        self.addToScreen()

class EnemyBullet(Bullet):
    # move towards the spaceship
    def move(self, spaceshipX, spaceshipY):
        self.positionY = self.positionY + self.stepSize
        self.addToScreen()

class ChasingBullet(Bullet):

    def euclidianDistance(self, x1, x2, y1, y2):
        distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        return distance

    # fire a bullet
    def move(self, spaceshipX, spaceshipY):
        moveLeft = self.euclidianDistance(spaceshipX, self.positionX - self.stepSize, spaceshipY, self.positionY + self.stepSize)
        moveRight = self.euclidianDistance(spaceshipX, self.positionX + self.stepSize, spaceshipY, self.positionY + self.stepSize)

        if moveLeft < moveRight:
            self.positionX = self.positionX - self.stepSize
        else:
            self.positionX = self.positionX + self.stepSize

        self.positionY = self.positionY + self.stepSize
        self.addToScreen()