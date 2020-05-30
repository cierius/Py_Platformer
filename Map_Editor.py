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

# Initializing variables
mouse_coords = ()
grid = None
bg_tile_objs = []

# List containing all of the addresses of the images to be loaded. Function finds them and adds them.
tile_files = []
# Dictionary for storing tiles that are loaded. Makes it easier to select tiles
imgs = {}


class Tile:
    def __init__(self, _x, _y, _w, _h, _tile_type):
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
        self.tile_type = _tile_type

    def render(self):
        if(self.tile_type == None):
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 1)
        else:
            screen.blit(self.tile_type, (self.x, self.y, self.w, self.h))

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


def create_bg_tiles():
    print("Creating Background")
    for column in range(int(SIZE[0]/64)):
        for row in range(int(SIZE[1]/64)):
            bg_tile_objs.append(Tile(column*64, row*64, 64, 64, imgs["Yellow.png"]))


def event_handler():
    global running, mouse_coords

    mouse_coords = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if(e.type == pygame.QUIT):
            running = False

        if(e.type == pygame.MOUSEBUTTONDOWN):
            print("Mouse click")

def update():
    pass


def graphics():
    # Renders the background tiles all the time
    for tile in bg_tile_objs:
        tile.render()

    # Renders the moused over grid tile
    for tile in Grid.grid_list:
        if(tile.mouse_over(mouse_coords[0], mouse_coords[1])):
            tile.render()

    # Clears the canvas and then colors it black allowing for new updates
    pygame.display.flip()
    screen.fill((128, 255, 255))


def find_images():
    global tile_files

    # Finds all the files in the specified directory that end with .png
    for f in glob.glob(f"{pathlib.Path().absolute()}\\Map_Editor_Assets\\Tiles\\*.png"):
        tile_files.append(f"{f}")


def load_image(file):
    image = pygame.image.load(file).convert_alpha()
    return image


def init():
    global screen, grid

    if(pygame.init()):
        screen = pygame.display.set_mode(SIZE, 0, 32)
        pygame.display.set_caption("Map Editor")

        find_images()

        for file in tile_files:
            # Adds the file name to the dict as the key and the img as the value
            imgs[file[str(pathlib.Path().absolute()).__len__()+25:]] = load_image(file)
            print(f"Loaded {file}!")

        create_bg_tiles()
        grid = Grid()

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
