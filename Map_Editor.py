# The purpose of this script is to launch it's own window and allow anyone to create
# a tile-based map. The map will be saved in a .map file using python's pickle module.
# This script is going to be fully self contained thus it might be a little messy but
# the point is just to be simple and functional.

import pygame
import sys

SIZE = (640, 640)

tile_files = ["Assets\Images\Background\Yellow.png", "Assets\Images\Tiles\Orange_Plat_Left.png",
              "Assets\Images\Tiles\Orange_Plat_Mid.png", "Assets\Images\Tiles\Orange_Plat_Right.png"]
loaded_tiles = []

bg_tile_objs = []

screen = None
disp_surface = None
running = False

class Tile:
    def __init__(self, _x, _y, _tile_type):
        self.x = _x
        self.y = _y
        self.tile_type = _tile_type

    def render(self):
        screen.blit(self.tile_type, (self.x, self.y, 64, 64))

def create_bg_tiles():
    for column in range(int(SIZE[0]/64)):
        for row in range(int(SIZE[1]/64)):
            bg_tile_objs.append(Tile(column*64, row*64, loaded_tiles[0]))


def event_handler():
    global running

    for e in pygame.event.get():
        if(e.type == pygame.QUIT):
            running = False

        if(e.type == pygame.MOUSEBUTTONDOWN):
            print("Mouse click")


def graphics():
    for tile in bg_tile_objs:
        tile.render()

    pygame.display.flip()
    screen.fill((128, 255, 255))


def load_image(file):
    image = pygame.image.load(file).convert_alpha()
    return image


def init():
    global screen, disp_surface

    if(pygame.init()):
        screen = pygame.display.set_mode(SIZE, 0, 32)
        disp_surface = pygame.Surface(SIZE)
        pygame.display.set_caption("Map Editor")

        for file in tile_files:
            loaded_tiles.append(load_image(file))
            print(f"Loaded {file}!")

        create_bg_tiles()
        return True
    return False

def main():
    global running

    if(init()): running = True

    while running:
        graphics()
        event_handler()

    pygame.quit()
    sys.exit()

if(__name__ == "__main__"):
    main()
