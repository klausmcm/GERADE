import pytest
from contextlib import ExitStack as does_not_raise

import CODER.exception as exc
import CODER.grid as grid


@pytest.mark.parametrize("grid_dimensions", [((1, 1)), ((2, 2)), ((1, 10)), ((10, 1))])
def test_grid_constructor(grid_dimensions):
    g = grid.Grid(*grid_dimensions)
    assert len(g.get_grid()) == grid_dimensions[1]
    for row in g.get_grid():
        assert len(row) == grid_dimensions[0]


@pytest.mark.parametrize(
    "grid_dimensions, object_dimensions, object_placement, expected_result",
    [
        ((5, 5), (1, 1), (0, 0), True),
        ((5, 5), (5, 5), (0, 0), True),
        ((5, 5), (4, 4), (0, 0), True),
        ((5, 5), (4, 4), (1, 1), True),
        ((5, 5), (5, 5), (1, 1), False),
        ((5, 5), (6, 5), (0, 0), False),
        ((5, 5), (5, 6), (0, 0), False),
        ((5, 5), (6, 6), (0, 0), False),
        ((5, 5), (1, 1), (5, 5), False),
    ],
)
def test_space_check(
    grid_dimensions, object_dimensions, object_placement, expected_result
):
    g = grid.Grid(*grid_dimensions)
    assert g.does_fit(object_placement, object_dimensions) is expected_result


@pytest.mark.parametrize(
    "grid_dimensions, object_dimensions, object_placement, force_overwrite, expected_grid, expected_exception",
    [
        (
            (3, 3),
            (3, 3),
            (0, 0),
            False,
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            does_not_raise(),
        ),
        (
            (3, 3),
            (6, 6),
            (1, 1),
            False,
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            pytest.raises(exc.CapacityError),
        ),
    ],
)
def test_reserve_space(
    grid_dimensions,
    object_dimensions,
    object_placement,
    force_overwrite,
    expected_grid,
    expected_exception,
):
    # TODO: try mocking the grid array
    g = grid.Grid(*grid_dimensions)
    with expected_exception:
        g.reserve_space(object_placement, object_dimensions, force_overwrite)
    assert g.get_grid() == expected_grid


@pytest.mark.parametrize(
    "grid_dimensions, dimensions_to_reserve, coordinates_to_reserve, dimensions_to_check, expected_coordinates, expected_exception",
    [
        ((4, 4), (0, 0), (0, 0), (1, 1), (0, 0), does_not_raise()),
        ((4, 4), (2, 2), (0, 0), (3, 3), (0, 0), pytest.raises(exc.CapacityError)),
        ((4, 4), (2, 2), (0, 0), (2, 2), (2, 0), does_not_raise()),
    ],
)
def test_get_available_space_coordinates(
    grid_dimensions,
    dimensions_to_reserve,
    coordinates_to_reserve,
    dimensions_to_check,
    expected_coordinates,
    expected_exception,
):
    g = grid.Grid(*grid_dimensions)
    g.reserve_space(
        coordinates_to_reserve, dimensions_to_reserve, force_overwrite=False
    )
    with expected_exception:
        available_coordinates = g.get_available_space_coordinates(dimensions_to_check)
        assert available_coordinates == expected_coordinates
