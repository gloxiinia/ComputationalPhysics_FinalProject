import math
import pygame
import pymunk
import pymunk.pygame_util
from cuenetics.cue import Cue
from menu import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cuenetics!")

        self.clock = pygame.time.Clock()
        self.FPS = 120

        #game variables
        self.diam = 40
        self.pocketDiam = 66
        self.force = 0
        self.forceMax = 10000 # alimit needs to be set to prevent tunneling
        self.forceDir = 1
        self.lives = 3
        self.balls = []
        self.potted_balls = []

        self.pockets =  [ (55, 55),
                          (665, 48),
                          (1225, 55),
                          (50, 655),
                          (671, 669),
                          (1230, 648)]
        
        self.cushions = [ [(103, 54), (127, 79), (608, 79), (630, 54)],
                          [(711, 54), (735, 79), (1150, 79), (1177, 54)],
                          [(104, 665), (127, 639),(611, 639), (631, 665)],
                          [(710, 665), (726, 639), (1152, 639), (1176, 665)],
                          [(53, 106), (78, 127), (78, 590), (53, 614)],
                          [(1227, 106), (1202, 127), (1202, 590), (1227, 614)]]
        #states
        self.paused = False
        self.running = True
        self.playing = True
        self.taking_shot = True
        self.powering_up = False
        self.cue_ball_potted = False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        
        #game window
        self.DISPLAY_W, self.DISPLAY_H, self.BOTTOM_PANEL = pygame.display.Info().current_w, pygame.display.Info().current_h, 60
        self.display = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H  + self.BOTTOM_PANEL), pygame.FULLSCREEN|pygame.SCALED)
        
        #fonts and colors
        self.font_name = "Lato"
        self.font = pygame.font.SysFont("Lato",30)
        self.largeFont = pygame.font.SysFont("Lato",60)
        self.BG, self.RED, self.WHITE = (0,0,0), (255,0,0), (255,255,255)
        self.curr_menu = MainMenu(self)

        #pymunk variables
        self.space = pymunk.Space()
        self.staticBody = self.space.static_body

        #images
        self.original_table_image = pygame.image.load("cuenetics/assets/images/table.png").convert_alpha()
        self.table_image = pygame.transform.scale(self.original_table_image, (1280, 720))
        self.cue_image = pygame.image.load("cuenetics/assets/images/cue.png").convert_alpha()
        self.ball_images = []
    
    def adding_ball_images(self):
        for i in range(1, 17):
            self.ball_image = pygame.image.load("cuenetics/assets/images/ball_" + str(i) + ".png").convert_alpha()
            self.ball_image = pygame.transform.scale(self.ball_image, (40, 40))
            self.ball_images.append(self.ball_image)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.START_KEY = True
                if event.key == pygame.K_DOWN:
                    self.START_KEY = True
                if event.key == pygame.K_UP:
                    self.START_KEY = True
                if event.key == pygame.K_SPACE:
                    self.paused = True

            if event.type == pygame.MOUSEBUTTONDOWN and self.taking_shot is True:
                self.powering_up = True
            if event.type == pygame.MOUSEBUTTONUP and self.taking_shot is True:
                self.powering_up = False

    #function to reset keys
    def reset_keys(self):        
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
    
    #function to draw text
    def draw_text(self, text, text_color, size, x, y):
        font = pygame.font.SysFont("Lato", size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    #function for creating the pool balls
    def create_ball(self, rad, pos):
        #defining the actual shape of the ball
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, rad)
        shape.mass = 5
        shape.elasticity = 0.8

        #adding friction to the ball using pivot joint
        pivot = pymunk.PivotJoint(self.staticBody, body, (0,0), (0,0))
        pivot.max_bias = 0 #disable joint correction
        pivot.max_force = 1000 #emulating linear friction, higher value, higher friction

        #adding body to the pymunk space
        self.space.add(body, shape, pivot)
        return shape

    def create_cushion(self, dimensions):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = ((0,0))
        shape = pymunk.Poly(body, dimensions)
        shape.elasticity= 0.8
        self.space.add(body, shape)

    def game_setup(self):
        rows = 5
        
        #pool balls
        #creating balls
        for column in range(5):
            for row in range (rows):
                pos = (250 + (column * (self.diam + 1)), 270 + (row * (self.diam + 1)) + (column * self.diam/2)) #x coordinate, y coordinate
                newBall = self.create_ball(self.diam/2, pos)
                self.balls.append(newBall)
            rows -= 1
        
        #creating ball images
        self.adding_ball_images()
        
        #cue ball
        pos = (888, self.DISPLAY_H/2)
        cue_ball = self.create_ball(self.diam/2, pos)
        self.balls.append(cue_ball)

        print(self.balls)
        print(self.ball_images)
        print(self.potted_balls)

        #pool cushions
        for c in self.cushions:
            self.create_cushion(c)

        #cue stick setup
        cue_stick = Cue(self.balls[-1].body.position)

        #power bar setup and creation
        powerbar = pygame.Surface((10, 20))
        powerbar.fill(self.RED)

        return cue_stick, powerbar


    def game_play(self, cue_stick, powerbar):
        clock = pygame.time.Clock()
        FPS = 150

        clock.tick(FPS)
        self.space.step(1/FPS)
        

        #drawing the pool table
        self.display.blit(self.table_image, (0,0))

        #checking if any balls have been potted (went into the pockets)
        for i, ball in enumerate(self.balls):
            for pocket in self.pockets:
                xBallDist = abs(ball.body.position[0] - pocket[0])
                yBallDist = abs(ball.body.position[1] - pocket[1])
                ballDist = math.sqrt((xBallDist **2) + (yBallDist**2))
                if ballDist <= self.pocketDiam /2:
                    #check if the potted ball was the cue ball
                    if i == len(self.balls) - 1:
                        self.lives -= 1
                        self.cue_ball_potted = True
                        ball.body.position = (-200,-200)
                        ball.body.velocity = (0,0)
                    else:
                        self.space.remove(ball.body)
                        self.balls.remove(ball)
                        self.potted_balls.append(self.ball_images[i])
                        self.ball_images.pop(i)

        #drawing the pool balls
        for i, ball in enumerate(self.balls):
            self.display.blit(self.ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

        #drawing the cue stick
        #checking if all pool balls have stopped moving
        self.taking_shot = True
        for ball in self.balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0: #checking for ball speed, int is used in cases where the velocity is a really low value close to 0
                self.taking_shot = False
        
        #calculating the cue stick angle
        if self.taking_shot is True and self.playing is True:
            if self.cue_ball_potted is True:
                #reposition cue ball
                self.balls[-1].body.position = (888, self.DISPLAY_H/2)
                self.cue_ball_potted = False

            mousePos = pygame.mouse.get_pos()

            cue_stick.rect.center = self.balls[-1].body.position #making sure the cue stick follows the cue ball

            xDist = self.balls[-1].body.position[0] - mousePos[0]
            yDist = -(self.balls[-1].body.position[1] - mousePos[1]) #invert it back bc pygame y coordinates are flipped
            cueAngle = math.degrees(math.atan2(yDist, xDist))
            cue_stick.update(cueAngle)
            cue_stick.draw(self.display)
        
        #powering up cue stick
        if self.powering_up is True and self.playing is True:
            self.force += 100 * self.forceDir
            if self.force >= self.forceMax or self.force < 0:
                self.forceDir *= -1
            #draawing the power bar
            for bar in range(math.ceil(self.force /2000)):
                self.display.blit(powerbar, (self.balls[-1].body.position[0] -30  + (bar*15), 
                                    self.balls[-1].body.position[1] + 30))

        elif self.powering_up is False and self.taking_shot is True:
            xImpulse = math.cos(math.radians(cueAngle))
            YImpulse = math.sin(math.radians(cueAngle))
            self.balls[-1].body.apply_impulse_at_local_point((self.force * -xImpulse, self.force * YImpulse), (0,0))
            self.force = 0 #resetting the force for the next power up
            self.forceDir = 1 #resetting the force direction to not get stuck in a loop
        
        #drawing the bottom section
        pygame.draw.rect(self.display, self.BG, (0, self.DISPLAY_H, self.DISPLAY_W, self.BOTTOM_PANEL))
        self.draw_text(("LIVES: " + str(self.lives)), self.WHITE, 60, self.DISPLAY_W - 200, self.DISPLAY_H + 10)
        
        #drawing the potted balls in the bottom section
        for i, ball in enumerate(self.potted_balls):
            self.display.blit(ball, ((10 + (i * 50)), (self.DISPLAY_H + 10)))

        #checking for game over
        if self.lives <= 0:
            self.draw_text("GAME OVER", self.WHITE, 60, self.DISPLAY_W/2 - 160, self.DISPLAY_H /2 -100 )
            self.playing = False
        
        #checking for win (all balls potted)
        if len(self.balls) == 1:
            self.draw_text("YOU ARE WIN :D", self.WHITE, 60, self.DISPLAY_W/2 - 160, self.DISPLAY_H /2 -100 )
            self.playing = False

    
    def game_loop(self, prep):
        
        while self.playing:
            self.game_play(prep[0], prep[1])
            self.check_events()
            
            
            pygame.display.update()
            # self.reset_keys()





