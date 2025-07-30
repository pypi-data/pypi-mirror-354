import pandas as pd
import pytest

from active_period_method.active_period_method import ActivePeriodMethod

# ----------------------- DEFINE TEST DATA ------------------------------------

START = "2023-01-01 08:00:00"

# Some entries before active period
PRE_SHIFTING_BOTTLENECK_ENTRIES = [
    {"station": "A", "timestamp": START, "status": 0},
    {"station": "B", "timestamp": START, "status": 1},
    {"station": "B", "timestamp": "2023-01-01 08:03:00", "status": 1},
    {"station": "A", "timestamp": "2023-01-01 08:05:00", "status": 0},
    {"station": "B", "timestamp": "2023-01-01 08:05:00", "status": 0},
]

# Same-length active period from 08:10:00 at stations 'A' and 'B'
SHIFTING_BOTTLENECK_ENTRIES = [
    {"station": "A", "timestamp": "2023-01-01 08:10:00", "status": 1},
    {"station": "B", "timestamp": "2023-01-01 08:10:00", "status": 1},
    {"station": "B", "timestamp": "2023-01-01 08:12:00", "status": 1},
    {"station": "B", "timestamp": "2023-01-01 08:15:00", "status": 1},
    {"station": "A", "timestamp": "2023-01-01 08:17:00", "status": 1},
    {"station": "A", "timestamp": "2023-01-01 08:19:00", "status": 1},
    {"station": "B", "timestamp": "2023-01-01 08:42:00", "status": 1},
    {"station": "A", "timestamp": "2023-01-01 08:55:00", "status": 1},
    {"station": "A", "timestamp": "2023-01-01 09:00:00", "status": 0},
    {"station": "B", "timestamp": "2023-01-01 09:00:00", "status": 0},
]

# Some entries after
POST_SHIFTING_BOTTLENECK_ENTRIES = [
    {"station": "A", "timestamp": "2023-01-01 09:03:00", "status": 1},
    {"station": "B", "timestamp": "2023-01-01 09:10:00", "status": 1},
    {"station": "A", "timestamp": "2023-01-01 09:10:00", "status": 0},
    {"station": "B", "timestamp": "2023-01-01 09:14:00", "status": 0},
    {"station": "B", "timestamp": "2023-01-01 09:16:00", "status": 1},
    {"station": "B", "timestamp": "2023-01-01 09:19:00", "status": 0},
]

SHIFTING_BOTTLENECK_DATA_2_STATIONS = [
    *PRE_SHIFTING_BOTTLENECK_ENTRIES,
    *SHIFTING_BOTTLENECK_ENTRIES,
    *POST_SHIFTING_BOTTLENECK_ENTRIES,
]


# Maps station names to their duplicates
STATION_COPIES = {
    "A": ["C", "D", "E", "F"],
    "B": ["G", "H", "I", "J"],
}


def add_duplicate_entries(
    entries: list[dict[str, str]], duplicate_map: dict[str, list[str]]
) -> list[dict[str, str]]:
    """Adds duplicate entries according to specified station names.

    Parameters
    ----------
    entries : list[dict[str, str]]
        List of station state entries to be duplicated.
    duplicate_map : dict[str, list[str]]
        Maps a station name to a list of other station names,
        for which duplicate entries are added.

    Returns
    -------
    duplicated_entries : list[dict[str, str]]
        List of station state entries with duplicates added.
    """
    duplicated_entries = entries[:]
    for entry in entries:
        new_stations = duplicate_map[entry["station"]]
        for new_station in new_stations:
            duplicated_entry = entry.copy()
            duplicated_entry["station"] = new_station
            duplicated_entries.append(duplicated_entry)
    return duplicated_entries


SHIFTING_BOTTLENECK_DATA_10_STATIONS = [
    # Add idle state entries for all copies at beginning
    *[
        {"station": station, "timestamp": START, "status": 0}
        for station in STATION_COPIES["A"] + STATION_COPIES["B"]
    ],
    *PRE_SHIFTING_BOTTLENECK_ENTRIES,
    *add_duplicate_entries(SHIFTING_BOTTLENECK_ENTRIES, STATION_COPIES),
    *POST_SHIFTING_BOTTLENECK_ENTRIES,
]


def filter_shifting_bottleneck_durations(df: pd.DataFrame, station: str) -> pd.Series:
    """Helper function to extract shifting bottleneck data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the bottleneck data.
    station : str
        The station for which to filter the data.

    Returns
    -------
    pd.Series
        Series containing the duration of the shifting bottleneck for the specified
        station.
    """
    return df[(df["station"] == station) & (df["bottleneck_type"] == "shifting")][
        "duration"
    ]


# ----------------------- TEST IMPLEMENTATION ---------------------------------


@pytest.mark.parametrize(
    "bottleneck_entries, other_stations",
    [
        (SHIFTING_BOTTLENECK_DATA_2_STATIONS, ["B"]),
        (
            SHIFTING_BOTTLENECK_DATA_10_STATIONS,
            ["B"] + STATION_COPIES["A"] + STATION_COPIES["B"],
        ),
    ],
)
def test_t4_same_length_shifting_bottleneck(
    bottleneck_entries: list[dict[str, str]],
    other_stations: list[str],
    active_period_method_factory: ActivePeriodMethod,
    station_states: callable,
) -> None:
    """
    Test the behavior of the active period method when two stations have the same
    length active periods in the same time period. Uses n stations (n=2, n=10).
    Asserts that the shifting bottleneck is recognized for the duration.

    Parameters
    ----------
    bottleneck_entries : list[dict[str, str]]
        List of bottleneck entries to be used for the test.
    other_stations : list[str]
        List of other stations.
    active_period_method_factory : ActivePeriodMethod
            A factory function to create an instance of the active period method.
    """

    apm: ActivePeriodMethod = active_period_method_factory(
        station_states_df=station_states(bottleneck_entries)
    )

    apm.calculate_momentary_bottlenecks()
    df = apm.calculate_average_bottlenecks()

    durations_a = filter_shifting_bottleneck_durations(df, "A")
    durations_others = [
        filter_shifting_bottleneck_durations(df, station) for station in other_stations
    ]

    # Assert that the shifting bottlenecks at other stations are the same
    for duration_of_other_station in durations_others:
        pd.testing.assert_series_equal(
            durations_a, duration_of_other_station, check_index=False
        )

    # Assert that there is one shifting bottleneck
    assert len(durations_a) == 1

    # Assert the correct value
    assert durations_a.item() == pd.Timedelta(minutes=50)
