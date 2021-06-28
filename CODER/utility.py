import pint

UREG = pint.UnitRegistry()


def convert_to_pixels(distance, dpi_single):
    """Convert any distance to pixels using the given pixel density.

    If the given distance is an integer, assume that the number is already the number of pixels.

    :param distance: The distance to convert into pixels.
    :type distance: str
    :param dpi_single: The pixel density to use for the conversion.
    :type dpi_single: int
    :return: The equivalent number of pixels.
    :rtype: int
    """
    if isinstance(distance, int):
        return distance
    return int(dpi_single * UREG.parse_expression(distance).to(UREG.inch).magnitude)
