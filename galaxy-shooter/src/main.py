
import pygame, random, math
from spaceship import Spaceship
from enemy import Enemy, SmartEnemy
from star import Star

# initialize pygame
pygame.init()

# screen size
gameScreenX = 800
gameScreenY = 600
normalEnemiesCount = 4
smartEnemiesCount = 1
startCount = 10

screen = pygame.display.set_mode((gameScreenX, gameScreenY))
scoreFont = pygame.font.Font('freesansbold.ttf', 32)

# background music
# Lobo Loco - Insterstellar Icebreaker (ID 1446)
pygame.mixer.music.load('../assets/background.mp3')
pygame.mixer.music.play(-1)

# game title
pygame.display.set_caption("Galaxy Shooter")

def getNewBackgroundColor():
    # r = random.randint(20, 30)
    # g = random.randint(50, 70)
    # b = random.randint(50, 70)
    return (19, 34, 59)

def euclidianDistance(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return distance

def showScore(score):
    scoreComponent = scoreFont.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreComponent, (10, gameScreenY - 40))

running = True
spaceship = Spaceship(screen, gameScreenX, gameScreenY)
enemies = []
smartEnemies = []
stars = []

while running:

    # background
    screen.fill(getNewBackgroundColor())
    if len(stars) < startCount:
        stars.append(Star(screen, gameScreenX, gameScreenY))
    
    for star in stars:
        star.move()
        if star.positionY > gameScreenY:
            stars.remove(star)

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
    if len(enemies) < normalEnemiesCount:
        enemies.append(Enemy(screen, gameScreenX, gameScreenY))
    
    if len(smartEnemies) < smartEnemiesCount:
        smartEnemies.append(SmartEnemy(screen, gameScreenX, gameScreenY))

    for enemy in enemies + smartEnemies:
        enemy.move()
        distanceToSpaceship = euclidianDistance(enemy.positionX, spaceship.positionX, 
                                                enemy.positionY, spaceship.positionY)

        if distanceToSpaceship < 500:
            enemy.fire()

        for bullet in enemy.bullets:
            bullet.move(spaceship.positionX, spaceship.positionY)
            hitDistance = euclidianDistance(spaceship.positionX, bullet.positionX, 
                                            spaceship.positionY, bullet.positionY)
            if hitDistance < 30:
                pygame.mixer.Sound('../assets/Gun+Reload.wav').play()
                enemy.bullets.remove(bullet)
                spaceship.rotate()

            if bullet.positionY > gameScreenY:
                enemy.bullets.remove(bullet)


    # fire the bullets and remove when out of the game space
    for bullet in spaceship.bullets:
        bullet.move()
        if bullet.positionY < 0:
            try:
                spaceship.bullets.remove(bullet)
            except ValueError as e:
                print('bullet was already removed') 
        
        # if the bullet hits any enemy
        for enemy in enemies:
            hitDistance = euclidianDistance(enemy.positionX, bullet.positionX, 
                                            enemy.positionY, bullet.positionY)
            if hitDistance < 30:
                enemies.remove(enemy)
                spaceship.bullets.remove(bullet)
                spaceship.score = spaceship.score + 1
    
    showScore(spaceship.score)
    pygame.display.update()
    # pygame.event.clear()

        