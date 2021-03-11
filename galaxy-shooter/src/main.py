
import pygame, random

# initialize pygame
pygame.init()

# screen size
gameScreenX = 800
gameScreenY = 600

screen = pygame.display.set_mode((gameScreenX, gameScreenY))

# game title
pygame.display.set_caption("Galaxy Shooter")

class Spaceship:
    stepSize = 5

    def __init__(self):
        self.bodyX = 50
        self.bodyY = 50
        self.body = pygame.image.load('spaceship.png')
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.spaceshipMovement = 'stopped'
        self.positionX = 400
        self.positionY = 500

    def addToScreen(self):
        screen.blit(self.body, (self.positionX, self.positionY))

    def moveLeft(self):
        # boundary on the left
        if self.positionX - self.stepSize > 0:
            self.positionX =  self.positionX - self.stepSize

    def moveRight(self):
        # boundary on the right
        if self.positionX + self.stepSize < gameScreenX - self.bodyX:
            self.positionX =  self.positionX + self.stepSize



class Enemy:
    stepSize = 2

    def __init__(self):
        self.bodyX = 50
        self.bodyY = 50
        self.body = pygame.image.load('enemy.png')
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.enemyMovement = 'left'
        self.positionX = random.randint(50, gameScreenX - 50)
        self.positionY = random.randint(0, 50)


    def move(self):
        screen.blit(self.body, (self.positionX, self.positionY))

        # decide which way to move
        if self.enemyMovement == 'right':
            self.positionX = self.positionX + self.stepSize
        elif self.enemyMovement == 'left':
                self.positionX = self.positionX - self.stepSize

        # bounce back from the boundary
        if self.positionX < 0:
            self.enemyMovement = 'right'
        elif self.positionX > gameScreenX - self.bodyX:
            self.enemyMovement = 'left'


def getNewBackgroundColor():
    r = random.randint(30, 50)
    g = random.randint(50, 70)
    b = random.randint(50, 70)
    return (r, g, b)

running = True
spaceship = Spaceship()
enemies = []

while running:

    screen.fill(getNewBackgroundColor())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_LEFT:
                spaceship.spaceshipMovement = 'left'

            if event.key == pygame.K_RIGHT:
                spaceship.spaceshipMovement = 'right'

        if event.type == pygame.KEYUP:   
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship.spaceshipMovement = 'stopped'

    if spaceship.spaceshipMovement == 'left':
        spaceship.moveLeft()
    elif spaceship.spaceshipMovement == 'right':
        spaceship.moveRight()

    # add spcaeship on the screen
    spaceship.addToScreen()

    if len(enemies) < 10:
        enemies.append(Enemy())
    
    for enemy in enemies:
        enemy.move()
        
    pygame.display.update()

        