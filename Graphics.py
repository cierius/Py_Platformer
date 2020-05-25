import Global
import pygame

from Global import Color

def graphics():
    pygame.draw.rect(Global.screen, Color.get("Teal"), (15, Global.test_y, 100, 100))

    pygame.display.flip() # flip swaps the buffer canvas
    Global.screen.fill(Color.get("Black"))
