import Global
import pickle

class Map:
    def __init__(self, _file, _grid):
        self.file = _file
        self.grid = _grid
        self.map = [] # List used to hold the tile objects

    def save(self):
        """
        Open file
        Pickle each square of self.grid into a tuple that has (x, y, tile_type),
        but tile_type needs to be converted into a number
        """
        pass


    def load(self):
        """
        Open file
        Unpickle file using string.split
        for each grid square need to decipher the tile_type num into its
        respective name and then create a tile object that is added to self.map
        return self.map
        """
        pass
