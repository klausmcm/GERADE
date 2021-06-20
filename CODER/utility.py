from PIL import Image
import numpy as np
import pint

import CODER.exception as exc


UREG = pint.UnitRegistry()


def convert_to_pixels(dpi, distance):
    """Convert any distance to pixels using the given pixel density.

    :param dpi: The pixel density to use for the conversion.
    :type dpi: int
    :param distance: The distance to convert into pixels.
    :type distance: str
    :return: The equivalent number of pixels.
    :rtype: int
    """
    if isinstance(distance, int):
        return distance
    return int(dpi * UREG.parse_expression(distance).to(UREG.inch).magnitude)


def _trim_vertical_whitespace(image):
    """Remove the top and bottom whitespace padding for the given image.

    :param image: The image to trim.
    :type image: numpy.ndarray
    :return: The trimmed image.
    :rtype: numpy.ndarray
    """
    # TODO: limitation is that the image must have whitespace at the top AND bottom - whitespace in only one area is currently not handled properly
    white_mask = image == 255
    white_rows = np.all(white_mask, axis=1)
    edges = np.diff(white_rows, axis=0)
    areas = np.nonzero(edges)[0]  # this returns the indexes of all the identified edges
    if len(areas) == 0 or len(areas) == 1:
        return image
    cropped_image = np.delete(
        image, slice(areas[len(areas) - 1] + 1, len(image)), 0
    )  # crop the bottom white border
    cropped_image = np.delete(
        cropped_image, slice(0, areas[0] + 1), 0
    )  # crop the top white border
    return cropped_image


def crop_whitespace(image):
    """Remove the whitespace padding for the given image.

    :param image: The image with the whitespace to be trimmed.
    :type image: numpy.ndarray
    :return: The image without whitespace padding.
    :rtype: numpy.ndarray
    """
    image = _trim_vertical_whitespace(image)
    image = _trim_vertical_whitespace(image.T)
    return image.T
