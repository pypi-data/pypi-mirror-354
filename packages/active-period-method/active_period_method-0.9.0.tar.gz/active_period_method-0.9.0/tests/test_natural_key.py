import pytest

from active_period_method.utils.natural_key import natural_key


@pytest.mark.parametrize(
    "input_list, expected_order",
    [
        (["M1", "M10", "M2", "M3"], ["M1", "M2", "M3", "M10"]),
        (
            ["Station2", "Station", "Station10", "Station1"],
            ["Station", "Station1", "Station2", "Station10"],
        ),
        (["A100", "A2", "A"], ["A", "A2", "A100"]),
        (["A", "A1", "B", "B2", "B5"], ["A", "A1", "B", "B2", "B5"]),
        (
            ["A1B2", "A1B10", "A1B"],
            ["A1B", "A1B2", "A1B10"],
        ),  # Only trailing numbers as int
    ],
)
def test_natural_key_sorting(input_list, expected_order):
    """
    Test that sorting strings using natural_key produces expected natural sort order.
    Only trailing numbers are considered for sorting.
    """
    sorted_list = sorted(input_list, key=natural_key)
    assert (
        sorted_list == expected_order
    ), f"Expected {expected_order} but got {sorted_list}"
