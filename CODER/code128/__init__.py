"""Code-128 barcode encoder

All needed by the user is done via the Code128Encoder class:

>>> encoder = Code128Encoder("HuDoRa")
>>> encoder.save("test.png")

Implemented by Helen Taylor for HUDORA GmbH.
Updated and ported to Python 3 by Michael Mulqueen for Method B Ltd.

Detailed documentation on the format here:
http://www.barcodeisland.com/code128.phtml
http://www.adams1.com/pub/russadam/128code.html

You may use this under a BSD License.
"""
import logging

from PIL import Image
import numpy as np
import pint

from .textencoder import TextEncoder
import CODER.utility as utility

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Code128Encoder:
    """Top-level class which handles the overall process of
    encoding input string and outputting the result"""

    def __init__(self, text, quiet_zone_width):
        """Constructor for a Code128 barcode.

        :param text: The text to be encoded.
        :type text: str
        :param quiet_zone_width: The width in modules for each quiet zone. The barcode has a leading and trailing quiet zone.
        :type quiet_zone_width: int
        """

        self.text = text
        encoder = TextEncoder()

        self.encoded_text = encoder.encode(
            self.text
        )  # 1 is a black bar and 0 is a white bar
        logging.debug("Encoded text is %s", self.encoded_text)

        self.checksum = self.calculate_check_sum()
        logging.debug("Checksum is %d", self.checksum)

        self.bars = encoder.get_bars(self.encoded_text, self.checksum)
        self.bars = np.array(
            [0] * quiet_zone_width + list(self.bars) + [0] * quiet_zone_width,
            dtype=np.uint8,
        )
        logging.debug("Bars: %s", self.bars)

        self.resized_bars = None

    def calculate_check_sum(self):
        """Calculate the check sum of the encoded text.
        Checksum is based on the input text and the starting code,
        and a mod103 algorithm is used"""

        checksum = self.encoded_text[0]

        for index, char in enumerate(self.encoded_text):
            if index > 0:
                checksum += index * char

        return checksum % 103

    def scale_barcode(self, width, height, dpi):
        """Scale the barcode to the given lengths.

        :param width: The desired width of the barcode. If rounding occurs, the barcode will be padded with whitespace.
        :type width: str or int
        :param height: The desired height of the barcode.
        :type height: str or int
        :param dpi: The dpi to apply to the barcode. Used for converting the lengths to pixels.
        :type dpi: tuple(int, int)
        """
        dpi_width, dpi_height = dpi
        width = utility.convert_to_pixels(width, dpi_width)
        height = utility.convert_to_pixels(height, dpi_height)
        width_multiplier = width // len(self.bars)

        # pad with whitespace to match the given width
        padding = width - (width_multiplier * len(self.bars))
        padding_left = padding // 2
        padding_right = padding - padding_left

        self.resized_bars = np.repeat(
            self.bars, width_multiplier, 0
        )  # stretch horizontally
        padded_bars = np.concatenate(
            (
                np.array([0 for _ in range(padding_left)], dtype=np.uint8),
                self.resized_bars,
                np.array([0 for _ in range(padding_right)], dtype=np.uint8),
            )
        )  # stretch vertically
        self.resized_bars = np.tile(padded_bars, (height, 1))

    def save_image(self, filepath):
        """Save the resized barcode to file at the given path.

        :param filepath: The file to save the barcode to.
        :type filepath: str
        """
        colors = np.copy(self.resized_bars)
        colors[self.resized_bars == 0] = 255  # RGB code for white is 255
        colors[self.resized_bars == 1] = 0  # RGB code for black is 0
        image = Image.fromarray(colors)
        image.save(filepath)
