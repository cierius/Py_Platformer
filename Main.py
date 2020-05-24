import pygame
import Global
import sys

from Logger import *
from Init import init
from Event_Handler import event_handler
from Graphics import graphics


# Constants
APP_NAME = "Py_Platformer"
SIZE = (3, 4)
SCALE = 200


# Inits pygame and gets the app all up and running
if(init((SIZE[0]*SCALE, SIZE[1]*SCALE), APP_NAME)):
    Global.running = True
    Log("Game is running!")

# Update method called every frame
def update():
    event_handler()
    graphics()

# Update method called 60 times per sec.
# Use for game mechanics.
def fixed_update():
    pass

def quit():
    Log("Closing Application")
    Global.running = False
    pygame.quit()
    sys.exit()



# I always have my main loop at the very bottom of my code.
# Prob not best practice but I find it useful in that I can just zoom to the
# end and find the loop.
while(Global.running):
    if(Global.shut_down_request): quit()
    update()
    fixed_update()
