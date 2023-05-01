import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#creating game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cuenetics!")

#creating pymunk space
space = pymunk.Space()

#adding friction
staticBody = space.static_body
drawOptions = pymunk.pygame_util.DrawOptions(screen)

#clock
clock = pygame.time.Clock()
FPS = 120

#colors
BG = (50,50,50)

#loading images
tableImage = pygame.image.load("cuenetics/assets/images/table.png").convert_alpha()
tableImage = pygame.transform.scale(tableImage, (1280, 720))

#function for creating the pool balls
def createBall(rad, pos):
    #defining the actual shape of the ball
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, rad)
    shape.mass = 5

    #adding friction to the ball using pivot joint
    pivot = pymunk.PivotJoint(staticBody, body, (0,0), (0,0))
    pivot.max_bias = 0 #disable joint correction
    pivot.max_force = 1000 #emulating linear friction, higher value, higher friction

    #adding body to the pymunk space
    space.add(body, shape, pivot)
    return shape

newBall = createBall(25, (300, 300))

cueBall = createBall(25, (600, 320))

#creating game loop
isRunning = True

while isRunning:

    
    clock.tick(FPS)
    space.step(1/FPS)

    #background filling
    screen.fill(BG)

    #drawing the pool table
    screen.blit(tableImage, (0,0))

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cueBall.body.apply_impulse_at_local_point((-1500, 0), (0,0))
        if event.type == pygame.QUIT:
            isRunning = False
    
    space.debug_draw(drawOptions)
    pygame.display.update()

pygame.quit


