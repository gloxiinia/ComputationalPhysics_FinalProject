from cuenetics.cue import Cue
from game import Game
import pygame
import math

g = Game()
prep = g.game_setup() # put this and the powerbar inside the class

while g.running:
    
    g.game_loop(prep)
    pygame.display.update()