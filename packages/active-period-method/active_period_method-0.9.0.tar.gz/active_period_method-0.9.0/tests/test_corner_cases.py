from pathlib import Path

import pytest

from active_period_method.active_period_method import (
    ONLY_ONE_MACHINE_WARNING,
    ActivePeriodMethod,
)

DATA_DIR = Path(__file__).parent / "data"
ONE_STATION_ONLY_CSV = DATA_DIR / "one_station_only.csv"
COMPATIBLE_SIMULTANEOUS_STATES_ACTIVE = DATA_DIR / "compatible_simultaneous_active.csv"
COMPATIBLE_SIMULTANEOUS_STATES_INACTIVE = (
    DATA_DIR / "compatible_simultaneous_inactive.csv"
)
INCOMPATIBLE_SIMULTANEOUS_STATES = DATA_DIR / "incompatible_simultaneous.csv"


def test_t1_one_station_only(
    station_states: callable,
    active_period_method_factory: ActivePeriodMethod,
) -> None:
    """
    Test the behavior of the active period method when only one station is present.
    This test checks if a warning is raised when the input data contains only
    one station.

    Parameters
    ----------
    station_states : callable
        A function to generate station states DataFrame.
    active_period_method_factory : ActivePeriodMethod
        A factory function to create an instance of the active period method.
    """
    with pytest.warns(UserWarning, match=ONLY_ONE_MACHINE_WARNING):
        active_period_method_factory(station_states(ONE_STATION_ONLY_CSV))


@pytest.mark.parametrize(
    "csv_file",
    [COMPATIBLE_SIMULTANEOUS_STATES_INACTIVE, COMPATIBLE_SIMULTANEOUS_STATES_ACTIVE],
)
def test_t2_identical_simultaneous_states(
    station_states: callable,
    active_period_method_factory: ActivePeriodMethod,
    csv_file: Path | list,
) -> None:
    """
    Test the behavior of the active period method when two identical states are logged.
    The duplicate state entry should be removed from the DataFrame.

    Parameters
    ----------
    station_states : callable
        A function to generate station states DataFrame.
    active_period_method_factory : ActivePeriodMethod
            A factory function to create an instance of the active period method.
    csv_file : Path | list
        The path to the CSV file containing station states or a list of DataFrames.
    """
    states_df = station_states(csv_file)
    apm = active_period_method_factory(states_df)
    assert (
        len(apm.station_states_df) == len(states_df) - 1
    )  # One entry (the duplicate) should be removed.


def test_t3_non_identical_simultaneous_states(
    station_states: callable,
    active_period_method_factory: ActivePeriodMethod,
) -> None:
    """
    Test the behavior of the active period method when two non-identical states are
    logged. A ValueError should be raised in this case.

    Parameters
    ----------
    station_states : callable
            A function to generate station states DataFrame.
    active_period_method_factory : ActivePeriodMethod
                A factory function to create an instance of the active period method.
    """
    with pytest.raises(ValueError):
        active_period_method_factory(station_states(INCOMPATIBLE_SIMULTANEOUS_STATES))
