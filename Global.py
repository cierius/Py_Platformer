# The point of this file is to contain all of the global variables needed
# across different scripts.

from Character import Character

Color = {
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Orange": (255, 128, 0),
    "Teal": (0, 255, 255),
    "Pink": (255, 0, 255)
}

running = False
shut_down_request = False

screen = None


# Character variables
player = Character(10, 10)

# Character movement
move_left = False
move_right = False
is_jumping = False
is_grounded = None
