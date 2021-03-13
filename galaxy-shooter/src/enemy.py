import pygame, random
from datetime import datetime
from bullet import EnemyBullet, ChasingBullet

class Enemy:
    stepSize = 0.4

    def __init__(self, screen, gameScreenX, gameScreenY):
        self.gameScreenX = gameScreenX
        self.gameScreenY = gameScreenY 
        self.screen = screen

        self.bodyX = 50
        self.bodyY = 50
        self.body = pygame.image.load('rocket.png')
        self.body = pygame.transform.rotate(self.body, 180)
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.enemyMovement = 'left'
        self.positionX = random.randint(50, gameScreenX - 50)
        self.positionY = random.randint(0, 50)
        self.lastBulletFiredTime = datetime.now()
        self.bullets = []

    def move(self):
        self.screen.blit(self.body, (self.positionX, self.positionY))

        # decide which way to move
        if self.enemyMovement == 'right':
            self.positionX = self.positionX + self.stepSize
        elif self.enemyMovement == 'left':
                self.positionX = self.positionX - self.stepSize

        # bounce back from the boundary
        if self.positionX < 0:
            self.enemyMovement = 'right'
        elif self.positionX > self.gameScreenX - self.bodyX:
            self.enemyMovement = 'left'

    def destroyed(self):
        self.body  = pygame.transform.scale(self.body, (10, 10))

    def canFire(self):
        # check if the enemy can fire 
        currentTime = datetime.now()
        if (currentTime - self.lastBulletFiredTime).total_seconds() > 10 :
            return True
        else:
            return False
    
    # fire a bullet
    def fire(self):
        if self.canFire():
            pygame.mixer.Sound('Gun+Silencer.wav').play()
            bullet = EnemyBullet(self.screen, self.positionX, self.positionY)
            self.lastBulletFiredTime = datetime.now()
            self.bullets.append(bullet)


class SmartEnemy(Enemy):
    # fire a bullet
    def fire(self):
        if self.canFire():
            pygame.mixer.Sound('Gun+Silencer.wav').play()
            bullet = ChasingBullet(self.screen, self.positionX, self.positionY)
            self.lastBulletFiredTime = datetime.now()
            self.bullets.append(bullet)