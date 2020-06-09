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

# App variables / constant(s)
SIZE = (640, 640)
screen = None
running = False
font = None

# Initializing variables
mouse_coords = (0, 0)
mouse_origin = (0, 0)
mouse_delta = (0, 0)

grid = None
grid_panning = False

bg_tile_objs = []
button_list = []

# List containing all of the addresses of the images to be loaded. Function finds them and adds them.
tile_files = []
# Dictionary for storing tiles that are loaded. Makes it easier to select tiles
imgs = {}

cur_tile = None


class Tile:
    def __init__(self, _x, _y, _w, _h, _tile_type):
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
        self.tile_type = _tile_type

    def render(self):
        if(self.tile_type != None):
            screen.blit(self.tile_type, (self.x, self.y, self.w, self.h))

    def outline(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 1)

    def mouse_over(self, _mx, _my):
        if(_mx >= self.x and _mx <= self.x + self.w):
            if(_my >= self.y and _my <= self.y + self.h):
                return True


class Grid:
    grid_list = []

    def __init__(self):
        print("Creating Grid")
        for column in range(int(SIZE[0]/16)):
            for row in range(int(SIZE[1]/16)):
                Grid.grid_list.append(Tile(column*16, row*16, 16, 16, None))

    def save(self):
        pass

    def load(self):
        pass


class Button:
    def __init__(self, _name, _x, _y, _w=32, _h=32, _img=None, _text=None, _color=(200, 200, 255), _fill=0):
        self.name = _name
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
        self.text = _text
        self.color = _color
        self.fill = _fill

        if(_img is not None):
            self.img = pygame.transform.scale(_img, (32, 32))
        else:
            self.img = _img


    def render(self):
        #Draws the select-able tiles
        if(self.img != None):
            pygame.draw.rect(screen, self.color, (self.x-3, self.y-3, self.w+6, self.h+6), self.fill)
            screen.blit(self.img, (self.x, self.y, self.w, self.h))

        #Draws the click-able buttons
        elif(self.text != None):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
            screen.blit(font.render(str(self.text), False, (0, 0, 0)), (self.x, self.y))

    def coll(self):
        if(mouse_coords[0] >= self.x and mouse_coords[0] <= self.x + self.w):
            if(mouse_coords[1] >= self.y and mouse_coords[1] <= self.y + self.h):
                return True


def create_buttons():
    global button_list

    button_list.append(Button("Save_Button", 100, 5, 100, 50, _text="Save", _color=(0, 0, 255)))

    i = 0
    for img in imgs:
        if(img != "Yellow.png"):
            button_list.append(Button(img, 13, 15+(47*i), _img=imgs[img]))
            print(img)
            i += 1


def create_bg_tiles():
    print("Creating Background")
    for column in range(int(SIZE[0]/64)):
        for row in range(int(SIZE[1]/64)):
            bg_tile_objs.append(Tile(column*64, row*64, 64, 64, imgs["Yellow.png"]))


def pan_grid(delta):
    global bg_tile_objs, Grid
    for tile in bg_tile_objs:
        tile.x += delta[0]
        tile.y += delta[1]

    for tile in Grid.grid_list:
        tile.x += delta[0]
        tile.y += delta[1]


def place_tile():
    for tile in Grid.grid_list:
        if(tile.mouse_over(mouse_coords[0], mouse_coords[1])):
            tile.tile_type = cur_tile


def erase_tile():
    for tile in Grid.grid_list:
        if(tile.mouse_over(mouse_coords[0], mouse_coords[1])):
            tile.tile_type = None


def update():
    global mouse_origin, mouse_delta

    if(grid_panning):
        mouse_delta = (mouse_coords[0] - mouse_origin[0],
                       mouse_coords[1] - mouse_origin[1])
        pan_grid(mouse_delta)
        mouse_origin = mouse_coords


def event_handler():
    global running, mouse_coords, mouse_origin, grid_panning, cur_tile

    mouse_coords = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if(e.type == pygame.QUIT):
            running = False

        if(e.type == pygame.MOUSEBUTTONDOWN):
            if(e.button == 1): #LMB
                for button in button_list:
                    if(button.coll() is True and button.img is not None):
                        for b in button_list: # I feel like there is a more effecient way to do this
                            if(b.text is None):
                                b.color = (200, 200, 255)

                        cur_tile = imgs[button.name]
                        button.color = (255, 255, 0)
                        print(f"Changed tile to {button.name}")

                        # return is used here to stop the place_tile from happening
                        return
                    elif(button.coll() is True and button.text is not None):
                        print(button.name)
                        # TODO: Add functions based on button.name

                        # return is same as before, stops tile from being placed
                        return

                place_tile()

            if(e.button == 2): #MMB
                mouse_origin = mouse_coords
                grid_panning = True

            if(e.button == 3): #RMB
                for button in button_list:
                    if(button.coll() is True):
                        return

                erase_tile()

        elif(e.type == pygame.MOUSEBUTTONUP):
            if(e.button == 2):
                grid_panning = False


def graphics():
    # Renders the background tiles all the time
    for tile in bg_tile_objs:
        tile.render()

    # Renders the moused over grid tile
    for tile in Grid.grid_list:
        if(tile.tile_type == None):
            if(tile.mouse_over(mouse_coords[0], mouse_coords[1])):
                tile.outline()
        else:
            tile.render()

    # Tile selector box
    pygame.draw.rect(screen, (100, 100, 100), (5, 5, 48, 512))

    for button in button_list:
        button.render()

    # Save button
    pygame.draw.rect(screen, (255, 255, 0), (5, 522, 64, 32))
    screen.blit(font.render("Save", False, (0, 0, 0)), (5, 522))

    # Clear button - Clears the screen of all tiles that were placed
    pygame.draw.rect(screen, (255, 0, 0), (5, 603, 64, 32))

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
    global screen, grid, cur_tile, font

    if(pygame.init()):
        screen = pygame.display.set_mode(SIZE, 0, 32)
        pygame.display.set_caption("Map Editor")
        font = pygame.font.SysFont("Arial", 18)

        find_images()

        for file in tile_files:
            # Adds the file name to the dict as the key and the img as the value
            imgs[file[str(pathlib.Path().absolute()).__len__()+25:]] = load_image(file)
            print(f"Loaded {file}!")

        create_bg_tiles()
        create_buttons()
        grid = Grid()

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

    pygame.quit()
    sys.exit()

if(__name__ == "__main__"):
    main()
