import pygame
import sys
import time

# My scripts below this
import Global

from Logger import *
from Init import init
from Event_Handler import event_handler
from Graphics import graphics
from Global import player


# Constants
APP_NAME = "Py_Platformer"
SIZE = (4, 3)
SCALE = 200


# Update method called every frame
def update():
    event_handler()
    graphics()


# Update method called 60 times per sec.
# Use for game mechanics.
def fixed_update():
    if(Global.move_left):
        player.move("Left")
    if(Global.move_right):
        player.move("Right")


def quit():
    Log("Closing Application")
    Global.running = False
    pygame.quit()
    sys.exit()


# I always have my main loop at the very bottom of my code.
# Prob not best practice but I find it useful in that I can just zoom to the
# end and find the loop.
def main():
    # variables for frame rate limitation
    start_frame = 0
    delta_time = 0
    frame_time = 0

    # Inits pygame and gets the app all up and running
    if(init((SIZE[0]*SCALE, SIZE[1]*SCALE), APP_NAME)):
        Global.running = True
        Log("Game is running!")

    while(Global.running):
        # Gets time at beginning of frame
        start_frame = time.time()

        if(Global.shut_down_request): quit()
        update()

        # Gets time at end of frame and then finds the diff
        delta_time = time.time() - start_frame
        frame_time += delta_time

        if(frame_time >= 0.0166): # 1 second divided by 60 frames = 0.0166...
            fixed_update()
            frame_time -= 0.0166


if __name__ == '__main__':
    main()
