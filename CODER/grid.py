import copy

import CODER.exception as exc


class Grid:
    def __init__(self, width, height):
        # [[0, 0, 0, 0, 0],
        #  [0, 1, 1, 0, 0],
        #  [0, 1, 1, 0, 0],
        #  [0, 1, 1, 0, 0],
        #  [0, 0, 0, 0, 0]]
        # 0 means AVAILABLE
        # 1 means RESERVED

        self._width = width
        self._height = height
        self._grid = [[0 for x in range(width)] for x in range(height)]

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_grid(self):
        return self._grid

    def does_fit(self, coordinates, dimensions):
        try:
            for y in range(dimensions[1]):
                for x in range(dimensions[0]):
                    if self._grid[y + coordinates[1]][x + coordinates[0]] == 1:
                        return False
        except IndexError:
            return False
        return True

    def reserve_space(self, coordinates, dimensions, force_overwrite=False):
        original = copy.deepcopy(self._grid)
        try:
            for y in range(dimensions[1]):
                for x in range(dimensions[0]):
                    if (
                        not force_overwrite
                        and self._grid[y + coordinates[1]][x + coordinates[0]] == 1
                    ):
                        raise exc.CapacityError(
                            f"Failed reserving space. Not enough space (coordinates: {coordinates}, dimensions: {dimensions})."
                        )
                    self._grid[y + coordinates[1]][x + coordinates[0]] = 1
        except IndexError:
            self._grid = original
            raise exc.CapacityError()

    def get_available_space_coordinates(self, dimensions):
        """Return coordinates for next available space for given dimensions.

        Search for next available space by traversing columns before rows (x before y).
        """
        for y in range(self._height):
            for x in range(self._width):
                if self.does_fit((x, y), dimensions):
                    return x, y

        raise exc.CapacityError(
            f"Not enough space available for given dimensions ({dimensions})."
        )
