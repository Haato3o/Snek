import pygame
from pygame.locals import *
import random

class Colors:
    def __init__(self):
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (38, 38, 38)
        self.RED = (255, 102, 102)
        self.GREEN = (102, 255, 137)

        self.BOARD_ALT0 = (99, 154, 69)
        self.BOARD_ALT1 = (102, 158, 71)
        self.BOARD_ALT2 = (106, 166, 74)
        self.SNAKE = (56, 129, 89)
        self.SNAKE2 = (63, 143, 99)
        self.BACKGROUND = self.BOARD_ALT0 #(5, 46, 34)
        self.APPLE = (172, 195, 64)
        self.MOUSE = (145, 165, 52)

class Mouse:
    def __init__(self, window):
        self.Colors = Colors()
        self.posX = 0
        self.posY = 0
        self.width = 32
        self.height = 32
        self.window = window

    def place(self):
        pygame.draw.rect(self.window, self.Colors.MOUSE, (self.posX, self.posY, self.width, self.height))

    def position(self):
        self.posX = random.randint(0, 19)*33
        self.posY = random.randint(0, 14)*33

class Apple:
    def __init__(self, window):
        self.Colors = Colors()
        self.posX = 0
        self.posY = 0
        self.width = 32
        self.height = 32
        self.window = window

    def place(self):
        pygame.draw.rect(self.window, self.Colors.APPLE, (self.posX, self.posY, self.width, self.height))

    def make(self):
        self.posX = random.randint(0, 19)*33
        self.posY = random.randint(0, 14)*33
        

class Snake:
    def __init__(self, window):
        self.posX = 330
        self.posY = 231
        self.speed = 1.0 # 1 square every 200 ms
        self.size = 0
        self.alive = True
        self.sizeArray = []
        self.window = window
        self.Colors = Colors()
        self.SafeLock = K_RIGHT
        self.LastPosition = K_RIGHT
        self.TILE_COLORS = {}

    def make(self):
        if self.size == 0:
            self.sizeArray.append((self.posX, self.posY, 32, 32))
        else:
            self.sizeArray.append(self.sizeArray[0])
        self.size += 1
        #print(self.size)
        pygame.draw.rect(self.window, self.Colors.SNAKE, self.sizeArray[len(self.sizeArray)-1])

    def updatePosition(self):
        for i in range(len(self.sizeArray)-1, 0, -1):
            self.sizeArray[i] = self.sizeArray[i-1]
            #print(f'[{i}] posX: {self.sizeArray[i][0]} -> {self.sizeArray[i-1][0]} | posY: {self.sizeArray[i][1]} -> {self.sizeArray[i-1][1]}')
        self.sizeArray[0] = (self.posX, self.posY, 32, 32)
        #print(self.sizeArray)
    
    def kill(self):
        self.size = 0
        self.sizeArray = []
        self.posX = 0
        self.posY = 0

    def checkIfAlive(self):
        if self.sizeArray[0] in self.sizeArray[1: len(self.sizeArray)]:
                self.alive = False

    def move(self, direction):
        if self.alive == False:
            return
        pygame.draw.rect(self.window, self.TILE_COLORS[str(self.sizeArray[len(self.sizeArray)-1])], self.sizeArray[len(self.sizeArray)-1])
        if direction == K_RIGHT:
            if self.LastPosition == K_LEFT:
                self.move(K_LEFT)    
                return
            self.posX += 33
            self.LastPosition = K_RIGHT
        elif direction == K_LEFT:
            if self.LastPosition == K_RIGHT:
                self.move(K_RIGHT)    
                return
            self.posX -= 33
            self.LastPosition = K_LEFT
        elif direction == K_UP:
            if self.LastPosition == K_DOWN:
                self.move(K_DOWN)    
                return
            self.posY -= 33
            self.LastPosition = K_UP
        elif direction == K_DOWN:
            if self.LastPosition == K_UP:
                self.move(K_UP)    
                return
            self.posY += 33
            self.LastPosition = K_DOWN
        if self.posX > 627 and self.LastPosition == K_RIGHT:
            self.posX = 0
        elif self.posX == -33 and self.LastPosition == K_LEFT:
            self.posX = 627
        if self.posY == -33 and self.LastPosition == K_UP:
            self.posY = 462
        elif self.posY > 462 and self.LastPosition == K_DOWN:
            self.posY = 0
        self.updatePosition()
        self.checkIfAlive()
        for snakePart in self.sizeArray:
            if self.sizeArray.index(snakePart) % 2 == 0: # Even
                pygame.draw.rect(self.window, self.Colors.SNAKE, snakePart)
            else:
                pygame.draw.rect(self.window, self.Colors.SNAKE2, snakePart)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.Colors = Colors()
        self.Name = 'Snek'
        self.Size = (660, 515)
        self.Window = pygame.display.set_mode(self.Size, 0, 32)
        self.Snek = Snake(self.Window)
        self.Apple = Apple(self.Window)
        self.Mouse = Mouse(self.Window)
        self.ApplesCounter = 0
        self.Score = 0
        self.Timer = 0
        self.lastKeyPressed = K_RIGHT
        self.lastDirection = K_RIGHT
        pygame.display.set_caption(self.Name)
        self.Window.fill(self.Colors.BACKGROUND)
        self.drawTable()
    
    def drawTable(self):
        posX = 0
        posY = 0
        for y in range(15):
            for x in range(20):
                rng = random.randint(0, 2)
                pygame.draw.rect(self.Window, eval(f'self.Colors.BOARD_ALT{rng}'),(posX, posY, 32, 32))
                self.Snek.TILE_COLORS[f'({posX}, {posY}, 32, 32)'] = eval(f'self.Colors.BOARD_ALT{rng}')
                posX += 33
            posY += 33
            posX = 0

    def Events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT and self.lastKeyPressed != K_RIGHT:
                    if self.lastKeyPressed == K_LEFT:
                        self.lastKeyPressed = K_LEFT
                    else:
                        self.lastDirection = self.lastKeyPressed
                        self.lastKeyPressed = K_RIGHT
                if event.key == K_LEFT and self.lastKeyPressed != K_LEFT:
                    if self.lastKeyPressed == K_RIGHT:
                        self.lastKeyPressed = K_RIGHT
                    else:
                        self.lastDirection = self.lastKeyPressed
                        self.lastKeyPressed = K_LEFT
                if event.key == K_DOWN and self.lastKeyPressed != K_DOWN:
                    if self.lastKeyPressed == K_UP:
                        self.lastKeyPressed = K_UP
                    else:
                        self.lastDirection = self.lastKeyPressed
                        self.lastKeyPressed = K_DOWN
                if event.key == K_UP and self.lastKeyPressed != K_UP:
                    if self.lastKeyPressed == K_DOWN:
                        self.lastKeyPressed = K_DOWN
                    else:
                        self.lastDirection = self.lastKeyPressed
                        self.lastKeyPressed = K_UP
                if event.key == K_r:
                    self.Restart()

    def Restart(self):
        self.Snek.kill()
        self.Snek.alive = True
        self.Snek.speed = 1.0
        self.Window.fill(self.Colors.BACKGROUND)
        self.drawTable()
        self.ApplesCounter = 0
        self.Score = 0
        self.Snek.posX = 330
        self.Snek.posY = 231
        self.lastKeyPressed = K_RIGHT
        self.initGame()

    def EndGame(self):
        self.Window.fill(self.Colors.BLACK)
        endFont = pygame.font.SysFont('Bahnschrift', 35)
        text = endFont.render(f'GAME OVER!', True, self.Colors.WHITE)
        score = endFont.render(f'Score: {self.Score}', True, self.Colors.WHITE)
        restartText = endFont.render(f'Press "R" to restart!', True, self.Colors.WHITE)
        self.Window.blit(text, (200, 20))
        self.Window.blit(score, (245, 210))
        self.Window.blit(restartText, (150, 300))

    def UpdateScore(self):
        pygame.draw.rect(self.Window, self.Colors.GRAY, (0, 495, 660, 20))
        scoreFont = pygame.font.SysFont('Bahnschrift', 15)
        Score = scoreFont.render(f'Score: {self.Score}', True, self.Colors.WHITE)
        self.Window.blit(Score, (0, 496))
        

    def initGame(self):
        self.UpdateScore()
        self.Snek.make()
        clock = pygame.time.Clock()
        while True:
            time = clock.tick()
            self.Timer += time
            self.Events()
            if self.Timer > int(250*self.Snek.speed):
                self.Snek.move(self.lastKeyPressed)
                self.Timer = 0
            #print(f'Snek X: {self.Snek.posX} | Snek Y: {self.Snek.posY}')
            #print(f'Apple X: {self.Apple.posX} | Apple Y: {self.Apple.posY}')
            if self.ApplesCounter == 0:
                self.Apple.make()
                while (self.Apple.posX, self.Apple.posY, 32, 32) in self.Snek.sizeArray:
                    self.Apple.make()
                self.Apple.place()
                self.ApplesCounter += 1
            if self.Snek.posX == self.Apple.posX and self.Snek.posY == self.Apple.posY:
                self.Snek.make()
                self.Score += 10
                self.UpdateScore()
                self.Snek.speed = 1-self.Score/1000
                self.ApplesCounter = 0
            if self.Snek.alive == False:
                self.EndGame()
            pygame.display.update()


if __name__ == '__main__':
    Game = Game()
    Game.initGame()
