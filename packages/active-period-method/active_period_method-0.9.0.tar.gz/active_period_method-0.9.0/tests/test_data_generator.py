import pytest

from active_period_method.utils.data_generator import (
    generate_mock_data,
    generate_time_series_varied_intervals,
)


@pytest.mark.parametrize(
    "stations, num_days, max_changes_per_day",
    [(1, 1, 1), (2, 2, 2), (3, 3, 3), (10, 10, 10)],
)
def test_generate_time_series_varied_intervals(
    stations: int, num_days: int, max_changes_per_day: int
) -> None:
    """
    Test that consecutive states within each station's time series are never the same
    for generate_time_series_varied_intervals.

    Parameters
    ----------
    stations : int
        Number of stations to generate time series for.
    num_days : int
        Number of days to generate time series data for.
    max_changes_per_day : int
        Maximum number of changes in status per day.
    """
    series_dict = generate_time_series_varied_intervals(
        stations=stations,
        num_days=num_days,
        max_changes_per_day=max_changes_per_day,
    )

    # For each machine's DataFrame, verify consecutive values differ.
    for station_key, df in series_dict.items():
        df_sorted = df.sort_values("timestamp")
        statuses = df_sorted["status"].to_list()
        for i in range(len(statuses) - 1):
            assert (
                statuses[i] != statuses[i + 1]
            ), f"Consecutive states same at index {i} for {station_key} in {df_sorted}."


@pytest.mark.parametrize(
    "stations, num_days, max_changes_per_day, seed",
    [(1, 1, 1, None), (2, 2, 2, 42), (3, 3, 3, 42), (10, 10, 10, 42)],
)
def test_generate_mock_data(
    stations: int, num_days: int, max_changes_per_day: int, seed: int | None
) -> None:
    """
    Test that consecutive states for each station in generate_mock_data never match.

    Parameters
    ----------
    stations : int
        Number of stations to generate data for.
    num_days : int
        Number of days to generate data for.
    max_changes_per_day : int
        Maximum number of changes in status per day.
    fixed_seed : int | None
        Seed for random number generator, by default None.
        If not None, the same data should be generated every time.
    """
    df = generate_mock_data(
        stations=stations,
        num_days=num_days,
        max_changes_per_day=max_changes_per_day,
        seed=seed,
    )

    # Group by station and check consecutive statuses within each group
    for station, group in df.groupby("station"):
        group_sorted = group.sort_values("timestamp")
        statuses = group_sorted["status"].to_list()
        for i in range(len(statuses) - 1):
            assert (
                statuses[i] != statuses[i + 1]
            ), f"Consecutive states are the same at index {i} for station {station}."

    # Create another df if fixed seed and check if they are equal
    if seed is not None:
        df2 = generate_mock_data(
            stations=stations,
            num_days=num_days,
            max_changes_per_day=max_changes_per_day,
            seed=seed,
        )
        assert df.equals(df2), "DataFrames are not equal when using a fixed seed."
