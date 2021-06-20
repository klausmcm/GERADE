import os

import pint
from PIL import Image


class Page:
    def __init__(self, width, height, dpi=(600, 600)):
        ureg = pint.UnitRegistry()
        try:
            self._width = (
                width
                if isinstance(width, int)
                else int(dpi[0] * ureg.parse_expression(width).to("inch").magnitude)
            )
            self._height = (
                height
                if isinstance(height, int)
                else int(dpi[1] * ureg.parse_expression(height).to("inch").magnitude)
            )
            self._dpi = dpi
            self._sections = []
            self._image = Image.new("RGB", (self._width, self._height), "white")
            self._pixels = [
                [0 for x in range(self._width)] for x in range(self._height)
            ]
        except pint.errors.UndefinedUnitError:
            pass

    def add_section(self, section, coordinates, force_placement=False):
        section_width = section.get_width()
        section_height = section.get_height()
        return

    def get_page_dimensions(self):
        """"""
        return self._width, self._height

    def save(self, filepath):
        """Write template image to an image file."""
        self._image.save(filepath, dpi=self._dpi)


p = Page("5 cm", "3 cm")
