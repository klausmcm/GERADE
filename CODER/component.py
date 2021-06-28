from abc import ABCMeta, abstractmethod
import io
import importlib.resources as resources
import shlex
import string
import subprocess
import tempfile

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import pint

# import CODER.exception as exc
import CODER.exception as exc
import CODER.utility as utility

UREG = pint.UnitRegistry()


class Component(metaclass=ABCMeta):
    def __init__(self, dpi=(600, 600)):
        self._dpi = dpi
        self._width = None
        self._height = None

    @abstractmethod
    def get_dimensions(self):
        pass

    @abstractmethod
    def save_image(self):
        pass

    def get_dpi(self):
        return self._dpi


class Barcode(Component):
    def __init__(self, text, dpi=(600, 600)):
        self._barcode_image = None  # numpy.ndarray
        self._text = text
        super().__init__(dpi)

    def get_text(self):
        return self._text

    def get_barcode_image(self):
        return self._barcode_image

    def save_image(self, filepath):
        image = Image.fromarray(self._barcode_image)
        image.save(filepath)

    def get_dimensions(self):
        return self._width, self._height

    def set_barcode_image(self, image):
        self._barcode_image = image


class DatamatrixBarcode(Barcode):
    def __init__(self, text):
        self._module_size = None
        super().__init__(text)

    @staticmethod
    def generate_barcode(text, module_size):
        """Generate a png image of a datamatrix barcode using `dmtxwrite`.
        Do not include whitespace padding with the generated barcode.

        :param text: The text to be encoded.
        :type text: str
        :param module_size: The module size for generating the barcode.
        :type module_size: int
        :return: Image of the barcode.
        :rtype: numpy.ndarray
        """
        # dmtx-utils
        cmd = " ".join(
            [
                "dmtxwrite",
                "-d",
                str(module_size),
                "-m",
                str(0)
                # str(int(self._margin_factor * module_size)),
            ]
        )
        out = subprocess.run(
            args=shlex.split(cmd),
            input=bytes(text, "utf-8"),
            text=False,
            check=True,
            capture_output=True,
        )  # contains stdout output which is a bytestring
        return np.asarray(Image.open(io.BytesIO(out.stdout)))

    @staticmethod
    def determine_max_datamatrix_module_size(text, max_width, max_height, dpi):
        """Determine the maximum module size that can be used for generating a barcode that fits within the given dimensions.

        :param max_width: The maximum width that the barcode can be.
        :type max_width: int or str
        :param max_height: The maximum height that the barcode can be.
        :type max_height: int or str
        :param dpi: The DPI for the image. This is needed so that distances that are not pixels can be converted to pixels.
        :type dpi: tuple(int, int)
        :return: Maximum module size that can be used to create a barcode that will fit within the constraints.
        :rtype: int
        """
        dpi_horizontal, dpi_vertical = dpi
        max_width = utility.convert_to_pixels(dpi_horizontal, max_width)
        max_height = utility.convert_to_pixels(dpi_vertical, max_height)
        module_size = 1
        while True:
            barcode_image = DatamatrixBarcode.generate_barcode(text, module_size)
            if barcode_image.width > max_width or barcode_image.height > max_height:
                module_size = module_size - 1
                if module_size == 0:
                    raise exc.CapacityError("Not enough space for datamatrix barcode.")
                return module_size
            module_size += 1


class Text(Component):
    def __init__(self, text, image_font=None):
        with resources.path("files", "DejaVuSansMono.ttf") as fid:
            self._font = (
                ImageFont.truetype(str(fid)) if image_font is None else image_font
            )
        self._text = str(text).split(
            "\n"
        )  # text is split on newline characters -> array of strings
        super().__init__()

    def determine_max_font_size(self, max_width, max_height):
        max_width = utility.convert_to_pixels(self._dpi[0], max_width)
        max_height = utility.convert_to_pixels(self._dpi[1], max_height)
        font_size = 1
        while True:
            font = self._font.font_variant(size=font_size)
            width = font.getsize(max(self._text, key=len))[0]
            height = font.getsize(string.ascii_letters + string.digits)[1]
            if width > max_width or height > max_height:
                font_size -= 1
                if font_size <= 0:
                    raise exc.CapacityError("Not enough space.")
                return font_size
            font_size += 1

    def get_dimensions(self):
        return self._width, self._height

    def generate_text(self, font_size):
        self._font = self._font.font_variant(size=font_size)
        width = self._font.getsize(max(self._text, key=len))[0]
        height = self._font.getsize(string.ascii_letters + string.digits)[1]
        im = Image.new("RGBA", (width, height * len(self._text)))
        for i, text_line in enumerate(self._text):
            line_im = Image.new("RGBA", (width, height))
            draw = ImageDraw.Draw(line_im)
            draw.text((0, 0), text_line, fill="black", font=self._font)
            im.paste(line_im, (0, i * height), mask=line_im)
        self._text_image = im
        self._width = self._text_image.width
        self._height = self._text_image.height

    def save_image(self, filepath):
        self._text_image.save(filepath)
