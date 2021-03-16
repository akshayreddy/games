
import pygame, random, math
from spaceship import Spaceship
from enemy import Enemy, SmartEnemy
from star import Star


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()

        # screen size
        self.gameScreenX = 800
        self.gameScreenY = 600
        self.normalEnemiesCount = 4
        self.smartEnemiesCount = 1
        self.startCount = 10

        self.screen = pygame.display.set_mode((self.gameScreenX, self.gameScreenY))

        # game title
        pygame.display.set_caption("Galaxy Shooter")
        self.scoreFont = pygame.font.Font('freesansbold.ttf', 20)
        self.healthFont = pygame.font.Font('freesansbold.ttf', 20)

        # background music
        # Lobo Loco - Insterstellar Icebreaker (ID 1446)
        pygame.mixer.music.load('../assets/background.mp3')
        pygame.mixer.music.play(-1)

        # game title
        pygame.display.set_caption("Galaxy Shooter")

        self.spaceship = Spaceship(self.screen, self.gameScreenX, self.gameScreenY)
        self.enemies = []
        self.smartEnemies = []
        self.stars = []


    def start(self):
        self.running = True
        self.run()

    def stop(self):
        self.running = False

    def getNewBackgroundColor(self):
        return (19, 34, 59)

    def euclidianDistance(self, x1, x2, y1, y2):
        distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        return distance

    def showScore(self, score):
        scoreComponent = self.scoreFont.render("Score: " + str(score), True, (255, 255, 255))
        self.screen.blit(scoreComponent, (5, self.gameScreenY - 40))

    def showHealth(self, health):
        healthComponent = self.healthFont.render("Health: " + str(health) + "%", True, (255, 255, 255))
        self.screen.blit(healthComponent, (10, self.gameScreenY - 60))

    def keyboardEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.spaceshipMovement = 'left'

                if event.key == pygame.K_RIGHT:
                    self.spaceship.spaceshipMovement = 'right'

                if event.key == pygame.K_a:
                    self.spaceship.fire()

            if event.type == pygame.KEYUP:   
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.spaceship.spaceshipMovement = 'stopped'

    def observeStars(self):
        if len(self.stars) < self.startCount:
            self.stars.append(Star(self.screen, self.gameScreenX, self.gameScreenY))
        
        for star in self.stars:
            star.move()
            if star.positionY > self.gameScreenY:
                self.stars.remove(star)

    def observeEnemies(self):
        # ensure min number of enemies
        if len(self.enemies) < self.normalEnemiesCount:
            self.enemies.append(Enemy(self.screen, self.gameScreenX, self.gameScreenY))
        
        if len(self.smartEnemies) < self.smartEnemiesCount:
            self.smartEnemies.append(SmartEnemy(self.screen, self.gameScreenX, self.gameScreenY))

        for enemy in self.enemies + self.smartEnemies:
            enemy.move()
            distanceToSpaceship = self.euclidianDistance(enemy.positionX, self.spaceship.positionX, 
                                                    enemy.positionY, self.spaceship.positionY)

            if distanceToSpaceship < 500:
                enemy.fire()

            for bullet in enemy.bullets:
                bullet.move(self.spaceship.positionX, self.spaceship.positionY)
                hitDistance = self.euclidianDistance(self.spaceship.positionX, bullet.positionX, 
                                                self.spaceship.positionY, bullet.positionY)
                if hitDistance < 30:
                    pygame.mixer.Sound('../assets/Gun+Reload.wav').play()
                    enemy.bullets.remove(bullet)
                    self.spaceship.health = self.spaceship.health - 10

                if bullet.positionY > self.gameScreenY:
                    enemy.bullets.remove(bullet)

    def observePlayer(self):

        if self.spaceship.spaceshipMovement == 'left':
                self.spaceship.moveLeft()
        elif self.spaceship.spaceshipMovement == 'right':
            self.spaceship.moveRight()

        # add spcaeship on the screen
        self.spaceship.addToScreen()


        # fire the bullets and remove when out of the game space
        for bullet in self.spaceship.bullets:
            bullet.move()
            if bullet.positionY < 0:
                try:
                    self.spaceship.bullets.remove(bullet)
                except ValueError:
                    print('bullet was already removed') 
            
            # if the bullet hits any enemy
            for enemy in self.enemies:
                hitDistance = self.euclidianDistance(enemy.positionX, bullet.positionX, 
                                                enemy.positionY, bullet.positionY)
                if hitDistance < 30:
                    self.enemies.remove(enemy)
                    self.spaceship.bullets.remove(bullet)
                    self.spaceship.score = self.spaceship.score + 1
        
        self.showScore(self.spaceship.score)
        self.showHealth(self.spaceship.health)

    def run(self):
        while self.running == True:

            # background
            self.screen.fill(self.getNewBackgroundColor())

            self.keyboardEvents()
            self.observePlayer()
            self.observeEnemies()
            self.observeStars()

            pygame.display.update()
            # pygame.event.clear()
            

game = Game()
game.start()