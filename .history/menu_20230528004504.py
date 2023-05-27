import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H /2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -100

    #helper functions
    def draw_cursor(self):
        self.game.draw_text("*", 50, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "start"
        self.start_x, self.start_y = self.mid_w, self.mid_h + 30
        self.options_x, self.options_y = self.mid_w, self.mid_h + 50
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 70
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 20, self.mid_w, self.mid_h - 20)
            self.game.draw_text("Start", 20, self.start_x, self.start_y)
            self.game.draw_text("Options", 20, self.options_x, self.options_y)
            self.game.draw_text("Credits", 20, self.credits_x, self.credits_y)
            self.game.draw_text("Quit", 20, self.quit_x, self.quit_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "start":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "options"
            elif self.state == "options":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "credits"
            elif self.state == "credits":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "quit"
            elif self.state == "quit":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "start"
        elif self.game.UP_KEY:
            if self.state == "start":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "quit"
            elif self.state == "options":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "start"
            elif self.state == "credits":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "options"
            elif self.state == "quit":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "credits"
    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "start":
                self.game.playing = True
            elif self.state == "options":
                pass
            elif self.state == "credits":
                pass
            elif self.state == "quit":
                pass
            self.run_display = False    