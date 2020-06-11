import Global
import pickle

class Map:
    def __init__(self, _x, _y, _file=None):
        self.file = _file
        self.grid = [] # List used to hold the tile objects

        if(self.file != None):
            self.load()

    def new_grid(self):
        print("Creating Grid!")
        for column in range(self.x):
            for row in range(self.y):
                self.grid.append(Tile(column*16, row*16, 16, 16, None))

    def save(self):
        """
        Open file
        Pickle each square of self.grid into a tuple that has (x, y, tile_type),
        but tile_type needs to be converted into a number
        """
        pass


    def load(self):
        print(f"Loading {self.file}!")
        """
        Open file
        Unpickle file using string.split
        for each grid square need to decipher the tile_type num into its
        respective name and then create a tile object that is added to self.map
        return self.map
        """
        pass
