from abc import ABCMeta, abstractmethod

import grid
import utility


class Tile(metaclass=ABCMeta):
    # to center an image, its top left coordinates can be calculated by floor(canvas width/2) - floor(image width/2)
    def __init__(self, width, height, dpi=(600, 600)):
        self._width = utility.convert_to_pixels(dpi[0], width)
        self._height = utility.convert_to_pixels(dpi[1], height)
        self._parts = []
        self._grid = grid.Grid(self._width, self._height)
