
import pygame, random, math
from datetime import datetime

# initialize pygame
pygame.init()

# screen size
gameScreenX = 800
gameScreenY = 600
numberOfEnemies = 3

screen = pygame.display.set_mode((gameScreenX, gameScreenY))
scoreFont = pygame.font.Font('freesansbold.ttf', 32)

# background music
# Lobo Loco - Insterstellar Icebreaker (ID 1446)
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)

# game title
pygame.display.set_caption("Galaxy Shooter")

class Spaceship:
    stepSize = 0.8

    def __init__(self):
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
        screen.blit(self.body, (self.positionX, self.positionY))

    def moveLeft(self):
        # boundary on the left
        if self.positionX - self.stepSize > 0:
            self.positionX =  self.positionX - self.stepSize

    def moveRight(self):
        # boundary on the right
        if self.positionX + self.stepSize < gameScreenX - self.bodyX:
            self.positionX =  self.positionX + self.stepSize

    # fire a bullet
    def fire(self):
        pygame.mixer.Sound('Gun+Silencer.wav').play()
        bullet = SpaceshipBullet(self.positionX, self.positionY)
        self.bullets.append(bullet)

class Enemy:
    stepSize = 0.4
    canFireTime = random.randint(4, 6) 

    def __init__(self):
        self.bodyX = 50
        self.bodyY = 50
        self.body = pygame.image.load('enemy.png')
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.enemyMovement = 'left'
        self.positionX = random.randint(50, gameScreenX - 50)
        self.positionY = random.randint(0, 50)
        self.lastBulletFiredTime = datetime.now()
        self.bullets = []


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

    def destroyed(self):
        self.body  = pygame.transform.scale(self.body, (10, 10))

    def canFire(self):
        # check if the enemy can fire 
        currentTime = datetime.now()
        if (currentTime - self.lastBulletFiredTime).total_seconds() > self.canFireTime:
            return True
        else:
            return False
    
    # fire a bullet
    def fire(self):
        if self.canFire():
            pygame.mixer.Sound('Gun+Silencer.wav').play()
            bullet = EnemyBullet(self.positionX, self.positionY)
            self.lastBulletFiredTime = datetime.now()
            self.bullets.append(bullet)


class Bullet:
    stepSize = 1

    def __init__(self, x, y):
        self.bodyX = 25
        self.bodyY = 25
        self.body = pygame.image.load('bullet.png')
        self.body  = pygame.transform.scale(self.body, (self.bodyX, self.bodyY))
        self.positionX = x
        self.positionY = y
    
    def addToScreen(self):
        screen.blit(self.body, (self.positionX, self.positionY))

class SpaceshipBullet(Bullet):
    # move towards the enemy
    def move(self):
        self.positionY = self.positionY - self.stepSize
        self.addToScreen()

class EnemyBullet(Bullet):
    # move towards the spaceship
    def move(self):
        self.positionY = self.positionY + self.stepSize
        self.addToScreen()


def getNewBackgroundColor():
    r = random.randint(20, 30)
    # g = random.randint(50, 70)
    # b = random.randint(50, 70)
    return (r, 20, 20)

def euclidianDistance(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return distance

def showScore(score):
    scoreComponent = scoreFont.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreComponent, (10, gameScreenY - 40))

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

            if event.key == pygame.K_a:
                spaceship.fire()

        if event.type == pygame.KEYUP:   
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship.spaceshipMovement = 'stopped'

    if spaceship.spaceshipMovement == 'left':
        spaceship.moveLeft()
    elif spaceship.spaceshipMovement == 'right':
        spaceship.moveRight()

    # add spcaeship on the screen
    spaceship.addToScreen()

    # ensure min number of enemies
    if len(enemies) < numberOfEnemies:
        enemies.append(Enemy())
    

    for enemy in enemies:
        enemy.move()
        distanceToSpaceship = euclidianDistance(enemy.positionX, spaceship.positionX, 
                                                enemy.positionY, spaceship.positionY)
        if distanceToSpaceship < 500:
            enemy.fire()

        for bullet in enemy.bullets:
            bullet.move()
            if bullet.positionY > gameScreenY:
                enemy.bullets.remove(bullet)
        

    # fire the bullets and remove when out of the game space
    for bullet in spaceship.bullets:
        bullet.move()
        if bullet.positionY < 0:
            spaceship.bullets.remove(bullet)
        
        # if the bullet hits any enemy
        for enemy in enemies:
            hitDistance = euclidianDistance(enemy.positionX, bullet.positionX, 
                                            enemy.positionY, bullet.positionY)
            if hitDistance < 30:
                pygame.mixer.Sound('Gun+Reload.wav').play()
                enemies.remove(enemy)
                spaceship.score = spaceship.score + 1
    
    showScore(spaceship.score)
    pygame.display.update()
    # pygame.event.clear()

        