import numpy as np
import pytest

import CODER.utility as utility


@pytest.mark.parametrize(
    "input_image, expected_trimmed_image",
    [
        (
            [
                [255, 255, 255, 255, 255, 255],  # trim
                [255, 255, 255, 255, 255, 255],  # trim
                [255, 255, 255, 255, 255, 255],  # trim
                [255, 0, 255, 0, 0, 255],
                [255, 255, 255, 255, 255, 255],
                [255, 255, 255, 255, 255, 255],
                [255, 0, 255, 0, 0, 255],
                [255, 255, 255, 255, 255, 255],  # trim
                [255, 255, 255, 255, 255, 255],  # trim
            ],
            [
                [255, 0, 255, 0, 0, 255],
                [255, 255, 255, 255, 255, 255],
                [255, 255, 255, 255, 255, 255],
                [255, 0, 255, 0, 0, 255],
            ],
        ),
        (
            [
                [255, 255, 0, 255],
                [255, 255, 0, 255],
                [255, 255, 0, 255],
            ],
            [
                [255, 255, 0, 255],
                [255, 255, 0, 255],
                [255, 255, 0, 255],
            ],
        ),
        (
            [
                [255, 255, 255, 255],
                [255, 255, 0, 255],
                [255, 255, 0, 255],
            ],
            [
                [255, 255, 255, 255],  # TODO: this row should be deleted
                [255, 255, 0, 255],
                [255, 255, 0, 255],
            ],
        ),
    ],
)
def test_trim_vertical_whitespace(input_image, expected_trimmed_image):
    # given
    input_image = np.array(input_image)
    expected_trimmed_image = np.array(expected_trimmed_image)
    # when
    trimmed_image = utility._trim_vertical_whitespace(input_image)
    # then
    assert np.array_equal(trimmed_image, expected_trimmed_image)


@pytest.mark.parametrize(
    "input_image, expected_trimmed_image",
    [
        (
            [
                [255, 255, 255, 255, 255, 255],  # trim
                [255, 255, 255, 255, 255, 255],  # trim
                [255, 255, 255, 255, 255, 255],  # trim
                [255, 0, 255, 0, 0, 255],
                [255, 255, 255, 255, 255, 255],
                [255, 255, 255, 255, 255, 255],
                [255, 0, 255, 0, 0, 255],
                [255, 255, 255, 255, 255, 255],  # trim
                [255, 255, 255, 255, 255, 255],  # trim
            ],
            [
                [0, 255, 0, 0],
                [255, 255, 255, 255],
                [255, 255, 255, 255],
                [0, 255, 0, 0],
            ],
        ),
        (
            [
                [255, 255, 0, 255],
                [255, 255, 0, 255],
                [255, 255, 0, 255],
            ],
            [
                [0],
                [0],
                [0],
            ],
        ),
    ],
)
def test_crop_whitespace(input_image, expected_trimmed_image):
    # given
    input_image = np.array(input_image)
    expected_trimmed_image = np.array(expected_trimmed_image)
    # when
    trimmed_image = utility.crop_whitespace(input_image)
    # then
    assert np.array_equal(trimmed_image, expected_trimmed_image)
