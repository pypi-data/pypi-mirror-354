import random

import pandas as pd


def generate_time_series_varied_intervals(
    stations: int, num_days: int, max_changes_per_day: int
) -> dict:
    """Generate time series with varied intervals for a given number of machines
    and days. Data is generated with random intervals and alternating states and
    is designed to appear somewhat realistic.

    Parameters
    ----------
    stations : int
        Number of machines.
    num_days : int
        Number of days.
    max_changes_per_day : int
        Maximum number of state changs per day.

    Returns
    -------
    dict
        Dictionary containing the pd.Series data.
    """
    # Define the start and end date for the time series
    start_date = "2023-01-01"
    end_date = pd.Timestamp(start_date) + pd.Timedelta(days=num_days - 1)

    # Generate the date range
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    series_dict = {}
    for key in range(1, stations + 1):
        time_series = []
        previous_value = 0
        for date in date_range:
            daily_values = []
            # Generate random times ensuring no overlap between changes
            min_interval = 1
            available_minutes = list(range(360, 1080 - min_interval, min_interval))
            times = sorted(random.sample(available_minutes, max_changes_per_day))

            # Convert minutes into timestamps
            times = [
                pd.Timestamp(date + pd.Timedelta(minutes=minute)) for minute in times
            ]

            for _ in range(max_changes_per_day):
                # Ensure alternation from the previous value
                value = 1 if previous_value == 0 else 0
                daily_values.append(value)
                previous_value = value

            # Append the -1 value at a fixed time (6pm)
            if previous_value == 1:
                times.append(pd.Timestamp(date + pd.Timedelta(hours=18)))
                daily_values.append(0)
                previous_value = 0

            # Create the pandas series
            series = pd.Series(data=daily_values, index=times)
            time_series.append(series)

        # Concatenate all daily series
        full_series = pd.concat(time_series)
        series_dict[f"M{key}"] = (
            full_series.to_frame()
            .reset_index()
            .rename(columns={0: "status", "index": "timestamp"})
        )

    return series_dict


def generate_mock_data(
    stations: int = 4,
    num_days: int = 3,
    max_changes_per_day: int = 4,
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate simple moke data with fixed seed for testing the active period method.

    Parameters
    ----------
    stations : int, optional
        Number of machines, by default 4.
    num_days : int, optional
        Number of days, by default 3.
    max_changes_per_day : int, optional
        Maximum number of state changes per day, by default 4.
    seed : int | None, optional
        Seed for random number generator, by default None,
        which means no fixed seed is used.

    Returns
    -------
    station_states_df : pd.DataFrame
        DataFrame containing the generated data.
    """
    # Set seed if given
    if seed is not None:
        random.seed(seed)

    # Generate data
    dfs = generate_time_series_varied_intervals(stations, num_days, max_changes_per_day)
    station_states_df = None
    for station, machine_states_df in dfs.items():
        machine_states_df["station"] = station
        if station_states_df is None:
            station_states_df = machine_states_df
        else:
            station_states_df = pd.concat(
                [station_states_df, machine_states_df], ignore_index=True
            )
    return station_states_df
