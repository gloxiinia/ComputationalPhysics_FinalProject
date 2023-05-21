import math
import pygame
import pymunk
import pymunk.pygame_util
import button

pygame.init()

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

cueImage = pygame.image.load("cuenetics/assets/images/cue.png").convert_alpha()

ballImages = []
for i in range(1, 17):
    ballImage = pygame.image.load("cuenetics/assets/images/ball_" + str(i) + ".png").convert_alpha()
    ballImage = pygame.transform.scale(ballImage, (40, 40))
    ballImages.append(ballImage)

#class for creating the cue
#cue is only a visual cue, not a pymunk object
class Cue():
    def __init__(self, pos):
        self.originalImage = cueImage # this is the original form/image of the cue itself
        self.angle = 0
        self.image = pygame.transform.rotate(self.originalImage, self.angle) #this is the image that will be rotating
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, angle):
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        surface.blit(self.image, 
                     (self.rect.centerx - self.image.get_width()/2,
                      self.rect.centery - self.image.get_height()/2
                      ))
        
#function to output text on screen
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

def createCushion(dimensions):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0,0))
    shape = pymunk.Poly(body, dimensions)
    shape.elasticity= 0.8
    space.add(body, shape)

#MENU SETUP
resumeBtn = button.Button(304, 125, resumeImage, 1)
optionsBtn = button.Button(315, 250, optionsImage, 1)
quitBtn = button.Button(330, 375, quitImage, 1)
videoBtn = button.Button(304, 125, videoImage, 1)
audioBtn = button.Button(315, 250, audioImage, 1)
backBtn = button.Button(330, 375, backImage, 1)

#GAME SETUP

#pool ball setup
balls = []
rows = 5

#creating balls
for column in range(5):
    for row in range (rows):
        pos = (250 + (column * (diam + 1)), 270 + (row * (diam + 1)) + (column * diam/2)) #x coordinate, y coordinate
        newBall = createBall(diam/2, pos)
        balls.append(newBall)
    rows -= 1

#cue ball
pos = (888, SCREEN_HEIGHT/2)
cueBall = createBall(diam/2, pos)
balls.append(cueBall)

#create table pockets
pockets = [
  (55, 55),
  (665, 48),
  (1225, 55),
  (50, 655),
  (671, 669),
  (1230, 648)
]

#cushion dimensions
cushions = [
  [(103, 54), (127, 79), (608, 79), (630, 54)],
  [(711, 54), (735, 79), (1150, 79), (1177, 54)],
  [(104, 665), (127, 639),(611, 639), (631, 665)],
  [(710, 665), (726, 639), (1152, 639), (1176, 665)],
  [(53, 106), (78, 127), (78, 590), (53, 614)],
  [(1227, 106), (1202, 127), (1202, 590), (1227, 614)]
]

for c in cushions:
    createCushion(c)

#cue stick setup
cueStick = Cue(balls[-1].body.position)

#power bar setup and creation
powerbar = pygame.Surface((10, 20))
powerbar.fill(RED)


#MAIN MENU

def mainMenu():
    pass

#GAME LOOP

isRunning = True

while isRunning:

    
    clock.tick(FPS)
    space.step(1/FPS)

    #background filling
    screen.fill(BG)

    #check if game is paused
    if isGamePaused is True:
        #check menu state
        if menuState == "main":
            #pause screen buttons drawn
            if resumeBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                isGamePaused = False
            if optionsBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                menuState = "options"
            if quitBtn.draw(screen) and not isBtnClicked:
                isRunning = False
        #check if options menu is open
        if menuState == "options":
            #options menu is drawn
            if videoBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                print("Video Settings")
            if audioBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                print("Audio Settings")
            if backBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                menuState = "main"
                
            

    else:
        
        #drawing the pool table
        screen.blit(tableImage, (0,0))

        #checking if any balls have been potted (went into the pockets)
        for i, ball in enumerate(balls):
            for pocket in pockets:
                xBallDist = abs(ball.body.position[0] - pocket[0])
                yBallDist = abs(ball.body.position[1] - pocket[1])
                ballDist = math.sqrt((xBallDist **2) + (yBallDist**2))
                if ballDist <= pocketDiam /2:
                    #check if the potted ball was the cue ball
                    if i == len(balls) - 1:
                        lives -= 1
                        isCueBallPotted = True
                        ball.body.position = (-200,-200)
                        ball.body.velocity = (0,0)
                    else:
                        space.remove(ball.body)
                        balls.remove(ball)
                        pottedBalls.append(ballImages[i])
                        ballImages.pop(i)

        #drawing the pool balls
        for i, ball in enumerate(balls):
            screen.blit(ballImages[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

        #drawing the cue stick
        #checking if all pool balls have stopped moving
        isTakingShot = True
        for ball in balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0: #checking for ball speed, int is used in cases where the velocity is a really low value close to 0
                isTakingShot = False
        
        #calculating the cue stick angle
        if isTakingShot is True and isGameRunning is True:
            if isCueBallPotted is True:
                #reposition cue ball
                balls[-1].body.position = (888, SCREEN_HEIGHT/2)
                isCueBallPotted = False

            mousePos = pygame.mouse.get_pos()

            cueStick.rect.center = balls[-1].body.position #making sure the cue stick follows the cue ball

            xDist = balls[-1].body.position[0] - mousePos[0]
            yDist = -(balls[-1].body.position[1] - mousePos[1]) #invert it back bc pygame y coordinates are flipped
            cueAngle = math.degrees(math.atan2(yDist, xDist))
            cueStick.update(cueAngle)
            cueStick.draw(screen)
        
        #powering up cue stick
        if isPoweringUp is True and isGameRunning is True:
            force += 100 * forceDir
            if force >= forceMax or force < 0:
                forceDir *= -1
            #draawing the power bar
            for bar in range(math.ceil(force /2000)):
                screen.blit(powerbar, (balls[-1].body.position[0] -30  + (bar*15), 
                                    balls[-1].body.position[1] + 30))

        elif isPoweringUp is False and isTakingShot is True:
            xImpulse = math.cos(math.radians(cueAngle))
            YImpulse = math.sin(math.radians(cueAngle))
            balls[-1].body.apply_impulse_at_local_point((force * -xImpulse, force * YImpulse), (0,0))
            force = 0 #resetting the force for the next power up
            forceDir = 1 #resetting the force direction to not get stuck in a loop
        
        #drawing the bottom section
        pygame.draw.rect(screen, BG, (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))
        drawText("LIVES: " + str(lives), largeFont, WHITE, SCREEN_WIDTH - 200, SCREEN_HEIGHT + 10)
        
        #drawing the potted balls in the bottom section
        for i, ball in enumerate(pottedBalls):
            screen.blit(ball, ((10 + (i * 50)), (SCREEN_HEIGHT + 10)))

        #checking for game over
        if lives <= 0:
            drawText("GAME OVER", largeFont, WHITE, SCREEN_WIDTH/2 - 160, SCREEN_HEIGHT /2 -100 )
            isGameRunning = False
        
        #checking for win (all balls potted)
        if len(balls) == 1:
            drawText("YOU ARE WIN :D", largeFont, WHITE, SCREEN_WIDTH/2 - 160, SCREEN_HEIGHT /2 -100 )
            isGameRunning = False

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isGamePaused = True
        if event.type == pygame.MOUSEBUTTONDOWN and isTakingShot is True:
            isPoweringUp = True
        if event.type == pygame.MOUSEBUTTONUP:
            isBtnClicked = False
        if event.type == pygame.MOUSEBUTTONUP and isTakingShot is True:
            isPoweringUp = False
        if event.type == pygame.QUIT:
            isRunning = False
        
    # space.debug_draw(drawOptions)
    pygame.display.update()

pygame.quit


