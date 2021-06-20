import pint

import CODER.grid as grid
import CODER.exception as exc
import utility

# https://www.geeksforgeeks.org/how-to-convert-images-to-numpy-array/

UREG = pint.UnitRegistry()


class Section:
    def __init__(self, width, height, dpi=(600, 600)):
        try:
            self._width = utility.convert_to_pixels(dpi[0], width)
            self._height = utility.convert_to_pixels(dpi[1], height)
            self._grid = grid.Grid(self._width, self._height)
            self._tiles = {}  # the key for each tile is its location
            self._dpi = dpi
        except pint.errors.UndefinedUnitError:
            pass

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_dpi(self):
        return self._dpi

    def get_grid(self):
        return self._grid

    def add_tile(self, tile, tile_coordinates=None):
        """
        :param tile_coordinates:
        :type tile_coordinates: tuple(int, int) or tuple(str, str) or tuple(int, str) or tuple(str, int)
        """
        x = None
        y = None
        if tile_coordinates is None:
            x, y = self._grid.get_available_space_coordinates(
                (tile.get_width(), tile.get_height())
            )
        else:
            x, y = tile_coordinates
            x = utility.convert_to_pixels(self._dpi[0], x)
            y = utility.convert_to_pixels(self._dpi[1], y)
        tile_coordinates = (x, y)
        self._tiles[tile_coordinates] = tile
