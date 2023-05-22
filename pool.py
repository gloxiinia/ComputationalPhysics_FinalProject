import math
import pygame
import pymunk
import pymunk.pygame_util
import button

pygame.init()

class Game():


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOTTOM_PANEL = 60

#creating game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
pygame.display.set_caption("Cuenetics!")

#creating pymunk space
space = pymunk.Space()

#adding friction
staticBody = space.static_body
drawOptions = pymunk.pygame_util.DrawOptions(screen)

#clock
clock = pygame.time.Clock()
FPS = 120

#variables for the game
diam = 40
pocketDiam = 66
force = 0
forceMax = 10000 # alimit needs to be set to prevent tunneling
forceDir = 1
lives = 3

#states
isTakingShot = True
isPoweringUp = False
isCueBallPotted = False
isGamePaused = False
isGameRunning = True
isBtnClicked = False
menuState = "main"

pottedBalls = []


#colors
BG = (50,50,50)
RED = (255,0,0)
WHITE = (255, 255, 255)

#fonts
font = pygame.font.SysFont("Lato",30)
largeFont = pygame.font.SysFont("Lato",60)

#loading images

#MENU BUTTONS
resumeImage = pygame.image.load("cuenetics/assets/images/buttons/button_resume.png").convert_alpha()
optionsImage = pygame.image.load("cuenetics/assets/images/buttons/button_options.png").convert_alpha()
quitImage = pygame.image.load("cuenetics/assets/images/buttons/button_quit.png").convert_alpha()
videoImage = pygame.image.load("cuenetics/assets/images/buttons/button_video.png").convert_alpha()
audioImage = pygame.image.load("cuenetics/assets/images/buttons/button_audio.png").convert_alpha()
backImage = pygame.image.load("cuenetics/assets/images/buttons/button_back.png").convert_alpha()

#POOL GAME
tableImage = pygame.image.load("cuenetics/assets/images/table.png").convert_alpha()
tableImage = pygame.transform.scale(tableImage, (1280, 720))

ballImages = []
for i in range(1, 17):
    ballImage = pygame.image.load("cuenetics/assets/images/ball_" + str(i) + ".png").convert_alpha()
    ballImage = pygame.transform.scale(ballImage, (40, 40))
    ballImages.append(ballImage)

    def drawText(text, font, textCol, x, y):
        img = font.render(text, True, textCol)
        screen.blit(img, (x, y))
        
    #function for creating the pool balls
    def createBall(rad, pos):
        #defining the actual shape of the ball
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, rad)
        shape.mass = 5
        shape.elasticity = 0.8

        #adding friction to the ball using pivot joint
        pivot = pymunk.PivotJoint(staticBody, body, (0,0), (0,0))
        pivot.max_bias = 0 #disable joint correction
        pivot.max_force = 1000 #emulating linear friction, higher value, higher friction

        #adding body to the pymunk space
        space.add(body, shape, pivot)
        return shape

    def createushion(dimensions):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = ((0,0))
        shape = pymunk.Poly(body, dimensions)
        shape.elasticity= 0.8
        space.add(body, shape)