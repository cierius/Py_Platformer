import Global
import pygame

from Global import Color, player

def graphics():
    player.render()

    pygame.display.flip() # flip swaps the buffer canvas
    Global.screen.fill(Color.get("Black"))
