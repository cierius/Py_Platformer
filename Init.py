import pygame
import Global

from Logger import *

def init(size, app_name):
    if(pygame.init()): Log("Pygame Initialized")

    Global.screen = pygame.display.set_mode(size, 0, 32)
    pygame.display.set_caption(app_name)

    return True
