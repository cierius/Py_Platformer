import pygame
import Global

def event_handler():
    for e in pygame.event.get():

        # If the X button is pressed on the window
        if(e.type == pygame.QUIT):
            Global.shut_down_request = True

        # Below here is where Keyboard input will be handled
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                Global.shut_down_request = True

            if(e.key == pygame.K_a or e.key == pygame.K_LEFT):
                Global.move_left = True
            if(e.key == pygame.K_d or e.key == pygame.K_RIGHT):
                Global.move_right = True
            if(e.key == pygame.K_SPACE or e.key == pygame.K_UP):
                pass

        if(e.type == pygame.KEYUP):
            if(e.key == pygame.K_a or e.key == pygame.K_LEFT):
                Global.move_left = False
            if(e.key == pygame.K_d or e.key == pygame.K_RIGHT):
                Global.move_right = False
