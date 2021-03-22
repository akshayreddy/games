import pygame, math
from datetime import datetime

class Bullet:
    stepSize = 1

    def __init__(self, screen, positionX, positionY):
        self.screen = screen
        self.bodyX = 25
        self.bodyY = 25
        self.body = pygame.image.load('../assets/bullet.svg')
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.positionX = positionX
        self.positionY = positionY
    
    def addToScreen(self):
        self.screen.blit(self.body, (self.positionX, self.positionY))

class SpaceshipBullet(Bullet):
    def __init__(self, screen, positionX, positionY):
        super().__init__(screen, positionX, positionY)
        self.body = pygame.image.load('../assets/bullet_blue.svg')
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))

    # move towards the enemy
    def move(self):
        self.positionY = self.positionY - self.stepSize
        self.addToScreen()

class EnemyBullet(Bullet):
    def __init__(self, screen, positionX, positionY):
        super().__init__(screen, positionX, positionY)
        self.body = pygame.image.load('../assets/bullet_yellow.svg')
        self.body = pygame.transform.rotate(self.body, 180)
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))

    # move towards the spaceship
    def move(self, spaceshipX, spaceshipY):
        self.positionY = self.positionY + self.stepSize
        self.addToScreen()

class ChasingBullet(Bullet):

    def __init__(self, screen, positionX, positionY):
        super().__init__(screen, positionX, positionY)
        self.body = pygame.image.load('../assets/bullet_red.svg')
        self.body = pygame.transform.rotate(self.body, 45)
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))

    def euclidianDistance(self, x1, x2, y1, y2):
        distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        return distance

    # fire a bullet
    def move(self, spaceshipX, spaceshipY):
        distanceToTheSpaceship = self.euclidianDistance(spaceshipX, self.positionX, spaceshipY, self.positionY)
        
        # chase unitl near
        if distanceToTheSpaceship > 150:
            moveLeft = self.euclidianDistance(spaceshipX, self.positionX - self.stepSize, spaceshipY, self.positionY + self.stepSize)
            moveRight = self.euclidianDistance(spaceshipX, self.positionX + self.stepSize, spaceshipY, self.positionY + self.stepSize)

            if moveLeft < moveRight:
                self.positionX = self.positionX - self.stepSize
            else:
                self.positionX = self.positionX + self.stepSize
        
        self.positionY = self.positionY + self.stepSize
        self.addToScreen()