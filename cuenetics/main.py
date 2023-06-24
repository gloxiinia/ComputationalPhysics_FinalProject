# IMPORTING THE MODULES
import math
import pygame
import pymunk
import pymunk.pygame_util
import button

from pygame import mixer
from inputBox import InputBox

#####################################################################################################################

pygame.init()

#SETTING SCREEN HEIGHT
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOTTOM_PANEL = 300

#CREATING THE GAME WINDOW
info = pygame.display.Info()
w = info.current_w
h = info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL),pygame.FULLSCREEN|pygame.SCALED)
icon = pygame.image.load("cuenetics/assets/images/icon.png").convert_alpha()
pygame.display.set_caption('Cuenetics!')
pygame.display.set_icon(icon)

#####################################################################################################################
#PYMUNK SETUP

#creating pymunk space
space = pymunk.Space()

#adding friction
staticBody = space.static_body
drawOptions = pymunk.pygame_util.DrawOptions(screen)

#####################################################################################################################
#GAME VARIABLES

#clock
clock = pygame.time.Clock()
FPS = 240

#variables for the game
diam = 45
rad = diam/2
pocketDiam = 66
mass = 5
elasticity = 1
maxFrictionForce = 1000
force = 0
forceMax = 20000 # alimit needs to be set to prevent tunneling
forceDir = 1
lives = 3
cueBallX = 888
cueBallY = SCREEN_HEIGHT/2
pottedBalls = []

#states
intro = True
freePlay = False
isTakingShot = True
isPoweringUp = False
isCueBallPotted = False
isRunning = False
isGamePaused = False
isGameRunning = True
isBtnClicked = False
menuState = "main"

#colors
BG = (27,64,121)
RED = (249,112,104)
WHITE = (255, 255, 255)

#textbox colors
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

# fonts
font = pygame.font.Font("cuenetics/assets/BalsamiqSans-Regular.ttf",22)
largeFont = pygame.font.Font("cuenetics/assets/BalsamiqSans-Regular.ttf",50)

#####################################################################################################################
# MUSIC SETUP
playlist = list()
playlist.append("cuenetics/assets/music/jazzyabstract.mp3")
playlist.append("cuenetics/assets/music/weeknds.mp3")
playlist.append("cuenetics/assets/music/bossanovacute.wav")

pygame.mixer.music.load ( playlist.pop() ) #get first track from the playlist
pygame.mixer.music.queue ( playlist.pop() ) #queue second song
pygame.mixer.music.set_endevent ( pygame.USEREVENT ) #setup end track event   
pygame.mixer.music.play() 

#####################################################################################################################
#LOADING IMAGES

#MENU BACKGROUNDS
mainMenu = pygame.image.load("cuenetics/assets/images/menu/menu_1.jpg").convert_alpha()
settingsMenu = pygame.image.load("cuenetics/assets/images/menu/menu_2.jpg").convert_alpha()
gameOver = pygame.image.load("cuenetics/assets/images/menu/game_over.jpg").convert_alpha()
gameOver = pygame.transform.smoothscale(gameOver, (1280, 720))

#TITLE IMAGE
titleImage = pygame.image.load("cuenetics/assets/images/cuenetics.png").convert_alpha()

#MENU BUTTONS
resumeImage = pygame.image.load("cuenetics/assets/images/buttons/resume_button.png").convert_alpha()
resumeImage = pygame.transform.smoothscale(resumeImage, (400, 100))
optionsImage = pygame.image.load("cuenetics/assets/images/buttons/settings_button.png").convert_alpha()
optionsImage = pygame.transform.smoothscale(optionsImage, (400, 100))
quitImage = pygame.image.load("cuenetics/assets/images/buttons/quit_button.png").convert_alpha()
quitImage = pygame.transform.smoothscale(quitImage, (400, 100))
startImage = pygame.image.load("cuenetics/assets/images/buttons/start_button.png").convert_alpha()
startImage = pygame.transform.smoothscale(startImage, (400, 100))
audioImage = pygame.image.load("cuenetics/assets/images/buttons/audio_button.png").convert_alpha()
audioImage = pygame.transform.smoothscale(audioImage, (400, 100))
mainMenuImage = pygame.image.load("cuenetics/assets/images/buttons/mainmenu_button.png").convert_alpha()
mainMenuImage = pygame.transform.smoothscale(mainMenuImage, (400, 100))
backImage = pygame.image.load("cuenetics/assets/images/buttons/back_button.png").convert_alpha()
backImage = pygame.transform.smoothscale(backImage, (400, 100))
freeplayImage = pygame.image.load("cuenetics/assets/images/buttons/freeplay_button.png").convert_alpha()
freeplayImage = pygame.transform.smoothscale(freeplayImage, (400, 100))
creditsImage = pygame.image.load("cuenetics/assets/images/buttons/credits_button.png").convert_alpha()
creditsImage = pygame.transform.smoothscale(creditsImage, (400, 100))

#CUE BUTTONS
classicImage = pygame.image.load("cuenetics/assets/images/buttons/classic_button.png").convert_alpha()
classicImage = pygame.transform.smoothscale(classicImage, (175, 50))
festiveImage = pygame.image.load("cuenetics/assets/images/buttons/festive_button.png").convert_alpha()
festiveImage = pygame.transform.smoothscale(festiveImage, (175, 50))
spaceImage = pygame.image.load("cuenetics/assets/images/buttons/space_button.png").convert_alpha()
spaceImage = pygame.transform.smoothscale(spaceImage, (175, 50))
barberImage = pygame.image.load("cuenetics/assets/images/buttons/barber_button.png").convert_alpha()
barberImage = pygame.transform.smoothscale(barberImage, (175, 50))
sharpImage = pygame.image.load("cuenetics/assets/images/buttons/sharp_button.png").convert_alpha()
sharpImage = pygame.transform.smoothscale(sharpImage, (175, 50))
pointyImage = pygame.image.load("cuenetics/assets/images/buttons/pointy_button.png").convert_alpha()
pointyImage = pygame.transform.smoothscale(pointyImage, (175, 50))

#POOL GAME
tableImage = pygame.image.load("cuenetics/assets/images/poolgame/table.png").convert_alpha()
tableImage = pygame.transform.smoothscale(tableImage, (1280, 720))

pathImage = pygame.image.load("cuenetics/assets/images/poolgame/dashed.png").convert_alpha()

cue1Image = pygame.image.load("cuenetics/assets/images/cues/cue1.png").convert_alpha()
cue1Image = pygame.transform.smoothscale(cue1Image, (2000, 80))
cue2Image = pygame.image.load("cuenetics/assets/images/cues/cue2.png").convert_alpha()
cue2Image = pygame.transform.smoothscale(cue2Image, (2000, 80))
cue3Image = pygame.image.load("cuenetics/assets/images/cues/cue3.png").convert_alpha()
cue3Image = pygame.transform.smoothscale(cue3Image, (2000, 80))
cue4Image = pygame.image.load("cuenetics/assets/images/cues/cue4.png").convert_alpha()
cue4Image = pygame.transform.smoothscale(cue4Image, (2000, 80))
cue5Image = pygame.image.load("cuenetics/assets/images/cues/cue5.png").convert_alpha()
cue5Image = pygame.transform.smoothscale(cue5Image, (2000, 80))
cue6Image = pygame.image.load("cuenetics/assets/images/cues/cue6.png").convert_alpha()
cue6Image = pygame.transform.smoothscale(cue6Image, (2000, 80))

ballImages = []
for i in range(1, 17):
    ballImage = pygame.image.load("cuenetics/assets/images/poolgame/ball_" + str(i) + ".png").convert_alpha()
    ballImage = pygame.transform.smoothscale(ballImage, (diam, diam))
    ballImages.append(ballImage)

#####################################################################################################################
#CLASSES AND FUNCTIONS

#CUE CLASS
#cue is only a visual cue, not a pymunk object
class Cue():
    def __init__(self, pos, image):
        self.originalImage = image # this is the original form/image of the cue itself
        self.angle = 0
        self.image = pygame.transform.rotate(self.originalImage, self.angle) #this is the image that will be rotating
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    def setImage(self, newImage):
        self.originalImage = newImage

    def update(self, angle):
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        surface.blit(self.image, 
                     (self.rect.centerx - self.image.get_width()/2,
                      self.rect.centery - self.image.get_height()/2
                      ))

# BALL CLASS   
class Ball():
    def __init__(self, pos, rad, mass, elasticity, maxFrictionForce):
        self.body = pymunk.Body()
        self.body.position = pos
        self.rad = rad
        self.shape = pymunk.Circle(self.body, rad)
        self.shape.mass = mass
        self.shape.elasticity = elasticity

        #adding friction to the ball using pivot joint
        self.pivot = pymunk.PivotJoint(staticBody, self.body, (0,0), (0,0))
        self.pivot.max_bias = 0 #disable joint correction
        self.pivot.max_force = maxFrictionForce #emulating linear friction, higher value, higher friction
    
    def addBall(self, space):
        space.add(self.body, self.shape, self.pivot)
        return self.shape

    def setMass(self, mass):
        self.shape.mass = mass
    
    def setRad(self, rad):
        self.rad = rad

    def setElasticity(self, elasticity):
        self.shape.elasticity = elasticity

    def setMaxForce(self, max_force):
        self.pivot.max_force = max_force

        
#function to output text on screen
def drawText(text, font, textCol, x, y):
    img = font.render(text, True, textCol)
    screen.blit(img, (x, y))

#function to create the cushions according to the dimensions
def createCushion(dimensions):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0,0))
    shape = pymunk.Poly(body, dimensions)
    shape.elasticity= 0.8
    space.add(body, shape)


#####################################################################################################################

#MENU SETUP
resumeBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2),250, resumeImage, 1)
editBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 375, resumeImage, 1)
optionsBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 625, optionsImage, 1)
quitBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 750, quitImage, 1)
startBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 375, startImage, 1)
freeplayBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 500, freeplayImage, 1)
creditsBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 500, creditsImage, 1)
mainMenuBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 375, mainMenuImage, 1)
audioBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 250, audioImage, 1)
backBtn = button.Button((SCREEN_WIDTH/2)-(resumeImage.get_width()/2), 500, backImage, 1)

#CUE SELECTION BUTTON
classicBtn = button.Button(75, SCREEN_HEIGHT + 210, classicImage, 1)
festiveBtn = button.Button(260, SCREEN_HEIGHT + 210, festiveImage, 1)
spaceBtn = button.Button(445, SCREEN_HEIGHT + 210, spaceImage, 1)
barberBtn = button.Button(630, SCREEN_HEIGHT + 210, barberImage, 1)
sharpBtn = button.Button(815, SCREEN_HEIGHT + 210, sharpImage, 1)
pointyBtn = button.Button(1000, SCREEN_HEIGHT + 210, pointyImage, 1)

#####################################################################################################################
#GAME SETUP

#pool ball setup
balls = []
rows = 5

#creating balls
for column in range(rows):
    for row in range (rows):
        pos = (250 + (column * (diam + 1)), 270 + (row * (diam + 1)) + (column * diam/2)) #x coordinate, y coordinate
        newBall = Ball(pos, rad, mass, elasticity, maxFrictionForce)
        newBall.addBall(space)
        balls.append(newBall)
    rows -= 1

#cue ball
pos = (cueBallX, cueBallY)
cueBall = Ball(pos, rad, mass, elasticity, maxFrictionForce)
cueBall.addBall(space)
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
cueStick = Cue(balls[-1].body.position, cue1Image)

#power bar setup and creation
powerbar = pygame.Surface((10, 20))
powerbar.fill(RED)

#ball path setup
ballPath = Cue(balls[-1].body.position, pathImage)

#input box setup
force_ip_box = InputBox(75, SCREEN_HEIGHT + 135, 50,32, font, COLOR_INACTIVE)
diam_ip_box = InputBox(300, SCREEN_HEIGHT + 135, 50, 32, font, COLOR_INACTIVE)
mass_ip_box = InputBox(525, SCREEN_HEIGHT + 135, 50, 32, font, COLOR_INACTIVE)
elasticity_ip_box = InputBox(750, SCREEN_HEIGHT + 135, 50, 32, font, COLOR_INACTIVE)
friction_ip_box = InputBox(975, SCREEN_HEIGHT + 135, 50, 32, font, COLOR_INACTIVE)
inputBoxes = [force_ip_box, diam_ip_box, mass_ip_box, elasticity_ip_box, friction_ip_box]


#####################################################################################################################

# MAIN MENU

while intro:
    screen.fill(BG)

    if menuState == "main":
        screen.blit(titleImage, ((SCREEN_WIDTH/2)-(titleImage.get_width()/2), 125))
        cue2Flip = pygame.transform.flip(cue2Image, True, False)
        cue4Flip = pygame.transform.flip(cue4Image, True, False)
        screen.blit(cue1Image, (-850, 385))
        screen.blit(cue2Flip, (170, 510))
        screen.blit(cue3Image, (-850, 635))
        screen.blit(cue4Flip, (170, 760))
        #pause screen buttons drawn
        if startBtn.draw(screen) and not isBtnClicked:
            isBtnClicked = True
            isRunning = True
            intro = False
        if freeplayBtn.draw(screen) and not isBtnClicked:
            isBtnClicked = True
            isRunning = True
            intro = False
            freePlay = True
                
        if optionsBtn.draw(screen) and not isBtnClicked:
            isBtnClicked = True
            menuState = "options"
                
        if quitBtn.draw(screen) and not isBtnClicked:
            pygame.quit()
            quit()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                isBtnClicked = False
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    pygame.display.update()
    clock.tick(15)

#####################################################################################################################

#GAME LOOP

while isRunning:

    clock.tick(FPS)
    space.step(1/FPS)

    #background filling
    screen.fill(BG)

    #check if game is paused
    if isGamePaused is True:
        #check menu state
        if menuState == "pause":
            #pause screen buttons drawn
            if resumeBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                isGamePaused = False
            if mainMenuBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                freeplay = False
            if creditsBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
            if optionsBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                menuState = "options"
            if quitBtn.draw(screen) and not isBtnClicked:
                isRunning = False
        #check if options menu is open
        if menuState == "options":
            #options menu is drawn
            if startBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                menuState = "game"
                print("Game Settings")
            if audioBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                menuState = "audio"
                print("Audio Settings")
            if backBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                menuState = "pause"
                
    #if it's not the main menu, then show this    
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
                        if freePlay == False:
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
            screen.blit(ballImages[i], (ball.body.position[0] - ball.rad, ball.body.position[1] - ball.rad))
        
        #drawing the cue stick
        #checking if all pool balls have stopped moving
        #updating the ball attributes
        isTakingShot = True
        for ball in balls:
            ball.setElasticity(elasticity)
            ball.setMass(mass)
            ball.setMaxForce(maxFrictionForce)
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0: #checking for ball speed, int is used in cases where the velocity is a really low value close to 0
                isTakingShot = False
        
        #calculating the cue stick angle
        if isTakingShot is True and isGameRunning is True:
            if isCueBallPotted is True:
                #reposition cue ball
                balls[-1].body.position = (cueBallX, cueBallY)
                isCueBallPotted = False

            mousePos = pygame.mouse.get_pos()

            cueStick.rect.center = balls[-1].body.position #making sure the cue stick follows the cue ball
            ballPath.rect.center = balls[-1].body.position #making sure aiming path follows the cue ball

            xDist = balls[-1].body.position[0] - mousePos[0]
            yDist = -(balls[-1].body.position[1] - mousePos[1]) #invert it back bc pygame y coordinates are flipped
            cueAngle = math.degrees(math.atan2(yDist, xDist))
            cueStick.update(cueAngle)
            cueStick.draw(screen)

            x2Dist = -(balls[-1].body.position[0] - mousePos[0])
            y2Dist = (balls[-1].body.position[1] - mousePos[1]) #not inverted back because we want the aim path to show up in front
            cueAngle2 = math.degrees(math.atan2(y2Dist, x2Dist))
            ballPath.update(cueAngle2)
            ballPath.draw(screen)


        #powering up cue stick
        if isPoweringUp is True and isGameRunning is True:
            force += 100 * forceDir
            if force >= float(forceMax) or force < 0:
                forceDir *= -1
            #draawing the power bar
            for bar in range(math.ceil(force / (float(forceMax)/5))):
                screen.blit(powerbar, (balls[-1].body.position[0] -30  + (bar*15), 
                                    balls[-1].body.position[1] + 30))
            

        elif isPoweringUp is False and isTakingShot is True:
            xImpulse = math.cos(math.radians(cueAngle))
            YImpulse = math.sin(math.radians(cueAngle))
            balls[-1].body.apply_impulse_at_local_point((force * -xImpulse, force * YImpulse), (0,0))
            force = 0 #resetting the force for the next power up
            forceDir = 1 #resetting the force direction to not get stuck in a loop
        
        #drawing the bottom section
        #if its classic mode, set the lives
        if freePlay == False:
            pygame.draw.rect(screen, BG, (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))
            drawText("LIVES: " + str(lives), largeFont, WHITE, SCREEN_WIDTH - 225, SCREEN_HEIGHT + 20)
        
        #if its free play, no lives
        else:
            pygame.draw.rect(screen, BG, (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))
            drawText("Cue Ball Velocity: " + str(round(math.sqrt((balls[-1].body.velocity[0])**2 + (balls[-1].body.velocity[1])**2), 3)), font, WHITE, SCREEN_WIDTH - 300, SCREEN_HEIGHT + 20)

            #INPUT CAPTIONS
            drawText("Max Force: " + str(forceMax) + " N", font, WHITE, 75, SCREEN_HEIGHT + 85)
            drawText("Ball Diameter: " + str(diam) + " m", font, WHITE, 300, SCREEN_HEIGHT + 85)
            drawText("Ball Mass: " + str(mass) + " kg", font, WHITE, 525, SCREEN_HEIGHT + 85)
            drawText("Ball Elasticity: " + str(elasticity), font, WHITE, 750, SCREEN_HEIGHT + 85)
            drawText("Ball Friction: " + str(maxFrictionForce) + " F/N", font, WHITE, 975, SCREEN_HEIGHT + 85)

            # CUE SELECTION
            if classicBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                cueStick.setImage(cue1Image)
                
            if festiveBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                cueStick.setImage(cue2Image)
                
            if spaceBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                cueStick.setImage(cue3Image)
                
            if barberBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                cueStick.setImage(cue4Image)

            if sharpBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                cueStick.setImage(cue5Image)

            if pointyBtn.draw(screen) and not isBtnClicked:
                isBtnClicked = True
                cueStick.setImage(cue6Image)

            #CHECKING INPUT BOXES FOR USER INPUT
            for box in inputBoxes:
                box.update()
                box.draw(screen)
                if box.active:
                    if box.get_text() == "" or box.get_text() == ' ':
                        pass
                    elif box.get_text() and box == inputBoxes[0]:
                        while box.get_text():
                            try:
                                num = float(box.get_text())
                            except ValueError:
                                break
                            forceMax = float(inputBoxes[0].get_text())
                            break

                    elif box.get_text() and box == inputBoxes[1]:
                        while box.get_text():
                            try:
                                num = float(box.get_text())
                            except ValueError:
                                break
                            diam = float(inputBoxes[1].get_text())
                            break
                        
                    elif box.get_text() and box == inputBoxes[2]:
                        while box.get_text():
                            try:
                                num = float(box.get_text())
                            except ValueError:
                                break
                            mass = float(inputBoxes[2].get_text())
                            break
                        
                    elif box.get_text() and box == inputBoxes[3]:
                        while box.get_text():
                            try:
                                num = float(box.get_text())
                            except ValueError:
                                break
                            elasticity = float(inputBoxes[3].get_text())
                            break
                        
                    elif box.get_text() and box == inputBoxes[4]:
                        while box.get_text():
                            try:
                                num = float(box.get_text())
                            except ValueError:
                                break
                            maxFrictionForce = float(inputBoxes[4].get_text())
                            break
                    else:
                        pass

        
        #drawing the potted balls in the bottom section
        for i, ball in enumerate(pottedBalls):
            screen.blit(ball, ((10 + (i * 50)), (SCREEN_HEIGHT + 20)))

        #checking for game over
        if lives <= 0:
            screen.blit(gameOver, (0,0))
            drawText("GAME OVER", largeFont, WHITE, SCREEN_WIDTH/2 - 160, SCREEN_HEIGHT /2 -100 )
            isGameRunning = False
        
        #checking for win (all balls potted)
        if len(balls) == 1:
            drawText("YOU WIN :D", largeFont, WHITE, SCREEN_WIDTH/2 - 160, SCREEN_HEIGHT /2 -100 )
            isGameRunning = False

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:  
            if len ( playlist ) > 0:     
                pygame.mixer.music.queue ( playlist.pop() )

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for box in inputBoxes:
                    if box.active == True:
                        continue 
                    else:
                        menuState = "pause"
                        isGamePaused = True
        if event.type == pygame.MOUSEBUTTONDOWN and isTakingShot is True:
            isPoweringUp = True
        if event.type == pygame.MOUSEBUTTONUP:
            isBtnClicked = False
        if event.type == pygame.MOUSEBUTTONUP and isTakingShot is True:
            isPoweringUp = False
        if event.type == pygame.QUIT:
            isRunning = False
        for box in inputBoxes:
            box.handle_event(event, font, COLOR_ACTIVE, COLOR_INACTIVE)
        
    
    pygame.display.update()

pygame.quit


