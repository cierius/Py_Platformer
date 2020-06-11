# The purpose of this script is to launch it's own window and allow anyone to create
# a tile-based map. The map will be saved in a .map file using python's pickle module.
# This script is going to be fully self contained thus it might be a little messy but
# the point is just to be simple and functional.

import pygame
import sys
import pickle
import os
import glob
import pathlib
import time


# App variables / constant(s)
SIZE = (640, 640)
screen = None
running = False
font = None

# Takes an input when starting the script. Will be used to load a map file so I don't have
# to create buttons for loading maps via GUI
starting_arg = sys.argv
map = None

# Initializing variables
mouse_coords = (0, 0)
mouse_origin = (0, 0)
mouse_delta = (0, 0)

grid = None
grid_panning = False

button_list = []
scroll_pos = 0

# List containing all of the addresses of the images to be loaded. Function finds them and adds them.
tile_files = []
# Dictionary for storing tiles that are loaded. Makes it easier to select tiles
imgs = {}

cur_tile = None


class Tile:
    def __init__(self, _x, _y, _w, _h, _tile_type, _tile_name):
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
        self.tile_type = _tile_type
        self.tile_name = _tile_name

    def render(self):
        if(self.tile_type != None):
            screen.blit(self.tile_type, (self.x, self.y, self.w, self.h))

    def outline(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 1)

    def mouse_over(self, _mx, _my):
        if(_mx >= self.x and _mx <= self.x + self.w):
            if(_my >= self.y and _my <= self.y + self.h):
                return True


class Map:
    def __init__(self, _file=time.time(), _x=32, _y=32):
        self.file = _file
        self.x = int(_x)
        self.y = int(_y)
        self.background = [] # List used to hold the backround objects
        self.grid = [] # List used to hold the tile objects

        if(self.load() == False):
            self.new_grid()
            self.new_background()
            self.save()

    def new_grid(self):
        print(f"Creating {self.x, self.y} Grid!")
        for column in range(self.x):
            for row in range(self.y):
                self.grid.append(Tile(column*16, row*16, 16, 16, None, None))


    def new_background(self, bg_img="Yellow.png"):
        print(f"Creating {self.x, self.y} Background!")

        # We can just call this method again if we want a different background
        # just have to input a different bg tile
        if(len(self.background) > 0):
            self.background.clear()

        for column in range(int(self.x/4)):
            for row in range(int(self.y/4)):
                self.background.append(Tile(column*64, row*64, 64, 64, imgs[bg_img], bg_img))


    def pan(self, delta):
        for tile in self.background:
            tile.x += delta[0]
            tile.y += delta[1]

        for tile in self.grid:
            tile.x += delta[0]
            tile.y += delta[1]

    def clear(self):
        print("Clearing Grid!")
        for t in self.grid:
            t.tile_type = None
            t.tile_name = None


    def save(self):
        print(f"Saving {self.file}!")

        f = open(f"Maps\\{self.file}.map", "wb")

        pickle.dump((len(self.grid), len(self.background)), f)

        for tile in self.grid:
            pickle.dump((tile.x, tile.y, tile.w, tile.h, tile.tile_name), f)

        for bg in self.background:
            pickle.dump((bg.x, bg.y, bg.tile_name), f)

        f.close()


    def load(self):
        print(f"Loading {self.file}!")

        # Searches the Maps folder to see if we already have a .map file
        for f in glob.glob(f"{pathlib.Path().absolute()}\\Maps\\*.map"):
            if(str(f) == f"{str(pathlib.Path().absolute())}\\Maps\\{self.file}.map"):
                s_time = time.time()
                file = open(f"Maps\\{self.file}.map", "rb")

                f_contents = pickle.load(file)

                for t in range(f_contents[0]):
                    temp = pickle.load(file)
                    print(temp)
                    if(temp[4] != None):
                        self.grid.append(Tile(temp[0], temp[1], temp[2], temp[3], imgs[temp[4]], temp[4]))
                    else:
                        self.grid.append(Tile(temp[0], temp[1], temp[2], temp[3], None, None))

                for bg in range(f_contents[1]):
                    temp = pickle.load(file)
                    self.background.append(Tile(temp[0], temp[1], 64, 64, imgs[temp[2]], temp[2]))

                file.close()
                print(f"Loading time: {time.time() - s_time}")
                return True

        print(f"No {self.file} Found! Creating New File Instead!")
        return False


class Button:
    def __init__(self, _name, _x, _y, _w=32, _h=32, _img=None, _text=None, _color=(200, 200, 255),
                 _fill=0, _selected=False):
        self.name = _name
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
        self.text = _text
        self.color = _color
        self.fill = _fill
        self.selected = _selected

        if(_img is not None):
            self.img = pygame.transform.scale(_img, (32, 32))
        else:
            self.img = _img


    def render(self):
        #Draws the select-able tiles
        if(self.img != None):
            if(self.selected):
                self.color = (255, 255, 0) # Yellow
            else:
                self.color = (200, 200, 255) # Gray

            pygame.draw.rect(screen, self.color, (self.x-3, self.y-3, self.w+6, self.h+6), self.fill)
            screen.blit(self.img, (self.x, self.y, self.w, self.h))

        #Draws the click-able buttons
        elif(self.text != None):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
            screen.blit(font.render(str(self.text), False, (0, 0, 0)), (self.x + 10, self.y + 5))

    def coll(self):
        if(mouse_coords[0] >= self.x and mouse_coords[0] <= self.x + self.w):
            if(mouse_coords[1] >= self.y and mouse_coords[1] <= self.y + self.h):
                return True


def create_buttons():
    global button_list

    button_list.append(Button("Save_Button", 5, 548, 64, 32, _text="Save", _color=(0, 255, 0)))
    button_list.append(Button("Clear_Button", 5, 603, 64, 32, _text="Clear", _color=(255, 0, 0)))

    i = 0
    for img in imgs:
        if(img != "Yellow.png"):
            button_list.append(Button(img, 13, 15+(47*i), _img=imgs[img]))
            print(img)
            i += 1


def scroll_buttons(dir):
    global button_list, scroll_pos
    for b in button_list:
        if(b.text == None):
            if(dir == "Up"):
                b.y -= 47
                scroll_pos -= 1

            elif(dir == "Down"):
                b.y += 47
                scroll_pos += 1


def place_tile():
    for tile in map.grid:
        if(tile.mouse_over(mouse_coords[0], mouse_coords[1])):
            tile.tile_type = cur_tile

            for key, val in imgs.items(): # Finds the key based on the value
                if(cur_tile == val):
                    tile.tile_name = key


def erase_tile():
    for tile in map.grid:
        if(tile.mouse_over(mouse_coords[0], mouse_coords[1])):
            tile.tile_type = None
            tile.tile_name = None


def update():
    global mouse_origin, mouse_delta

    if(grid_panning):
        mouse_delta = (mouse_coords[0] - mouse_origin[0],
                       mouse_coords[1] - mouse_origin[1])
        map.pan(mouse_delta)
        mouse_origin = mouse_coords


def event_handler():
    global running, mouse_coords, mouse_origin, grid_panning, cur_tile

    mouse_coords = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if(e.type == pygame.QUIT):
            running = False

        if(e.type == pygame.MOUSEBUTTONDOWN):
            button_state = pygame.mouse.get_pressed()

            if(button_state == (1, 0, 1)): #LMB and RMB for use on laptop / with no MMB
                mouse_origin = mouse_coords
                grid_panning = True

            elif(e.button == 1): #LMB
                for button in button_list: #this for loop tests all buttons, tile buttons and UI buttons
                    # Tile buttons
                    if(button.coll() is True and button.img is not None):
                        for b in button_list: # I feel like there is a more effecient way to do this
                            if(b.text is None):
                                b.selected = False

                        cur_tile = imgs[button.name]
                        button.selected = True
                        print(f"Changed tile to {button.name}")

                        # return is used here to stop the place_tile from happening
                        return

                        # UI Buttons
                    elif(button.coll() is True and button.text is not None):
                        #print(button.name)

                        if(button.name == "Save_Button"):
                            map.save()
                        elif(button.name == "Clear_Button"):
                            map.clear()
                        # return is same as before, stops tile from being placed
                        return

                place_tile()

            elif(e.button == 2): #MMB
                mouse_origin = mouse_coords
                grid_panning = True

            elif(e.button == 3): #RMB
                for button in button_list:
                    if(button.coll() is True): # if click on any button don't erase a tile
                        return

                erase_tile()

            elif(e.button == 4): # Mousewheel forward
                print("MWF")
                scroll_buttons("Up")

            elif(e.button == 5):
                print("MWB")
                scroll_buttons("Down")

        elif(e.type == pygame.MOUSEBUTTONUP):
            button_state = pygame.mouse.get_pressed()

            if(button_state != (1, 0, 1)): #LMB and RMB
                grid_panning = False

            if(e.button == 2): # MMB
                grid_panning = False


def graphics():
    # Renders the background tiles all the time
    for tile in map.background:
        tile.render()

    # Renders the moused over grid tile
    for tile in map.grid:
        if(tile.tile_type == None):
            if(tile.mouse_over(mouse_coords[0], mouse_coords[1])):
                tile.outline()
        else:
            tile.render()

    # Tile selector box
    pygame.draw.rect(screen, (100, 100, 100), (5, 5, 48, 522))

    for button in button_list:
        button.render()

    # Clears the canvas and then colors it black allowing for new updates
    pygame.display.flip()
    screen.fill((128, 255, 255)) # Light blue


def find_images():
    global tile_files

    # Finds all the files in the specified directory that end with .png
    for f in glob.glob(f"{pathlib.Path().absolute()}\\Map_Editor_Assets\\Tiles\\*.png"):
        tile_files.append(f"{f}")


def load_image(file):
    image = pygame.image.load(file).convert_alpha()
    return image


def init():
    global screen, map, cur_tile, font

    if(pygame.init()):
        screen = pygame.display.set_mode(SIZE, 0, 32)
        pygame.display.set_caption("Map Editor")
        font = pygame.font.SysFont("Arial", 18)

        find_images()

        for file in tile_files:
            # Adds the file name to the dict as the key and the img as the value
            imgs[file[str(pathlib.Path().absolute()).__len__()+25:]] = load_image(file)
            print(f"Loaded {file}!")

        create_buttons()

        # Creates / Loads the actual map file
        if(len(starting_arg) == 2): # 1 Input
            if(starting_arg[1].isnumeric()):
                map = Map(_x=starting_arg[1], _y=starting_arg[1])
            else:
                map = Map(_file=starting_arg[1])

        elif(len(starting_arg) == 3): # 2 Inputs
            if(starting_arg[1].isnumeric() and starting_arg[2].isnumeric()):
                map = Map(_x=starting_arg[1], _y=starting_arg[2])
            else:
                map = Map(_file=starting_arg[1], _x=starting_arg[2], _y=starting_arg[2])

        elif(len(starting_arg) == 4): # 3 Inputs
            map = Map(_file=starting_arg[1], _x=starting_arg[2], _y=starting_arg[3])

        else: # 0 Inputs
            map = Map()

        cur_tile = imgs["Orange_Plat_Mid.png"]

        return True
    return False

def main():
    global running

    if(init()): running = True

    while running:
        event_handler()
        graphics()
        update()

    map.save()
    pygame.quit()
    sys.exit()

if(__name__ == "__main__"):
    main()
