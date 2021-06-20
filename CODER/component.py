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


class Code128Barcode(Barcode):
    def __init__(self, text):
        super().__init__(text)

    @staticmethod
    def generate_barcode(text, width, height, dpi):
        """Generates a png image using `barcode`.

        Save the image in the barcode object as a PIL Image.
        Parse the given lengths and convert to mm which is the unit of measurement that `barcode` expects.

        :param text: The text to encode.
        :type text: str
        :param width: Desired width of the barcode. The width of the generated barcode may not match exactly but will not exceed the given width.
        :type width: int or str
        :param height: Desired height of the barcode. Unlike the width, the generated barcode will have the given height.
        :type height: int or str
        :param dpi: The DPI for the image. Needed to convert the width and height into mm.
        :type dpi: tuple(int, int)
        :return: Image of the barcode.
        :rtype: numpy.ndarray
        """
        # barcode to generate
        # zbarimg to verify
        dpi_horizontal, dpi_vertical = dpi
        height_pixels = (
            height
            if isinstance(height, int)
            else utility.convert_to_pixels(dpi_vertical, height)
        )
        width = (
            float(((width / dpi_horizontal) * UREG.inch).to(UREG.mm).magnitude)
            if isinstance(width, int)
            else UREG(width).to(UREG.mm).magnitude
        )  # convert width to mm
        height = (
            float(((height / dpi_vertical) * UREG.inch).to(UREG.mm).magnitude)
            if isinstance(height, int)
            else UREG(height).to(UREG.mm).magnitude
        )  # convert height to mm
        if width <= 0 or height <= 0:
            raise exc.CapacityError("Not enough space for Code128 barcode.")
        cmd_create = " ".join(
            [
                "barcode",
                "-n",
                "-b",
                str(text),
                "-e",
                "128",
                "-S",
                "-u",
                "mm",
                "-g",
                str(width)
                + "x"
                + str(1000)
                + "+0+0",  # height is set to 1000 here - the image will be stretched to the given height later
            ]
        )  # the width and height is given as mm to the barcode command
        out = subprocess.run(
            args=shlex.split(cmd_create),
            input=bytes(text, "utf-8"),
            text=False,
            check=True,
            capture_output=True,
        )
        cmd_convert = " ".join(
            [
                "convert",
                "-density",
                str(dpi_horizontal),
                "-",
                "-colorspace",
                "RGB",
                "PNG:-",
            ]
        )
        out = subprocess.run(
            args=shlex.split(cmd_convert),
            input=out.stdout,
            text=False,
            check=True,
            capture_output=True,
        )
        barcode_image = Image.open(io.BytesIO(out.stdout))
        barcode_image_array = np.asarray(barcode_image)
        barcode_image_array = np.tile(
            barcode_image_array[int(len(barcode_image_array) / 2)], (height_pixels, 1)
        )  # take the middle row of the barcode and stretch to the given height
        barcode_image_array = utility.crop_whitespace(barcode_image_array)

        return barcode_image_array

    @staticmethod
    def determine_max_width(text, max_width, dpi):
        """Determine the width that needs to be passed into `barcode` in order to generate a Code128 barcode that is equal or close to the given width.

        The width passed into `barcode` creates a barcode with the given width but includes whitespace padding around the barcode.
        The barcode itself has a width that is less than the given width.

        :param max_width: The width limit for the generated barcode.
        :type max_width: str or int
        :return: The width in pixels that needs to be passed into `barcode` in order to generate a barcode that close or equal to `max_width` (excluding the whitespace padding).
        :rtype: int
        """

        # TODO: This can take a very long time to compute. Try a binary search approach instead.
        # Lower bound would the given width and the upper bound could be set to 10x the lower bound.
        dpi_horizontal, dpi_vertical = dpi
        max_width = utility.convert_to_pixels(dpi_horizontal, max_width)
        width = max_width
        height = utility.convert_to_pixels(
            dpi_vertical, "3 cm"
        )  # the height is arbitrary since the barcode is freely adjustable in the vertical direction
        while True:
            barcode_image = Code128Barcode.generate_barcode(text, width, height, dpi)
            barcode_width, _ = barcode_image.shape
            if barcode_width <= max_width:
                width += 1
            if barcode_width > max_width:
                barcode_image = Code128Barcode.generate_barcode(
                    text, width - 1, height, dpi
                )
                if Code128Barcode.is_barcode_valid(Image.fromarray(barcode_image)):
                    return width - 1
                raise exc.CapacityError(f"{max_width} is not enough space.")

    @staticmethod
    def is_barcode_valid(image):
        with tempfile.NamedTemporaryFile(suffix=".png") as fid:
            image.save(fid.name)
            cmd = " ".join(["zbarimg", "-q", fid.name])
            verify = subprocess.run(shlex.split(cmd), check=True, capture_output=True)
            return verify.returncode == 0


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
