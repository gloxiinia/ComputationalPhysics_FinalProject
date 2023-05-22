import pygame
from menu import *

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = "Lato"
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.curr_menu = MainMenu(self)

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text("Thanks for playing", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()

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

    #function to reset keys
    def reset_keys(self):        
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
    
    #function to draw text
    def draw_text(self, text, size, x, y):
        font = pygame.font.SysFont(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)



