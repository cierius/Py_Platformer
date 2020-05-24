import pygame
import Global

def event_handler():
    for e in pygame.event.get():

        # If the X button is pressed on the window
        if(e.type == pygame.QUIT):
            Global.shut_down = True

        # Below here is where Keyboard input will be handled
        elif(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                Global.shut_down = True
