"""
This script is a simple test for validating the correctness of the
active period method calculation
"""

from pathlib import Path

import pandas as pd
import pytest

from active_period_method.active_period_method import ActivePeriodMethod
from active_period_method.utils.data_generator import generate_mock_data


@pytest.fixture
def preprocess_states_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Fixture to provide sample data for testing the preprocessing of station states.

    Returns
    -------
    sample_station_states : pd.DataFrame
        A DataFrame with duplicate consecutive statuses.
    expected_preprocessed_old_df : pd.DataFrame
        Expected DataFrame when using the old implementation (sorted by station then
        timestamp).
    expected_preprocessed_new_df : pd.DataFrame
        Expected DataFrame when using the new implementation (sorted only by timestamp).
    """
    # Sample input data
    test_data = {
        "station": ["A", "A", "A", "B", "B", "B"],
        "timestamp": [
            "2023-01-01 08:00:00",
            "2023-01-01 08:05:00",
            "2023-01-01 08:10:00",
            "2023-01-01 08:00:00",
            "2023-01-01 08:03:00",
            "2023-01-01 08:05:00",
        ],
        "status": [0, 0, 1, 1, 1, 0],
    }
    sample_station_states = pd.DataFrame(test_data)
    sample_station_states["timestamp"] = pd.to_datetime(
        sample_station_states["timestamp"]
    )

    # Expected DataFrame for the old implementation
    old_data = {
        "station": ["A", "A", "B", "B"],
        "timestamp": [
            pd.Timestamp("2023-01-01 08:00:00"),
            pd.Timestamp("2023-01-01 08:10:00"),
            pd.Timestamp("2023-01-01 08:00:00"),
            pd.Timestamp("2023-01-01 08:05:00"),
        ],
        "status": [0, 1, 1, 0],
    }
    expected_preprocessed_old_df = pd.DataFrame(old_data)

    # Expected DataFrame for the new implementation
    new_data = {
        "station": ["A", "B", "B", "A"],
        "timestamp": [
            pd.Timestamp("2023-01-01 08:00:00"),
            pd.Timestamp("2023-01-01 08:00:00"),
            pd.Timestamp("2023-01-01 08:05:00"),
            pd.Timestamp("2023-01-01 08:10:00"),
        ],
        "status": [0, 1, 0, 1],
    }
    expected_preprocessed_new_df = pd.DataFrame(new_data)

    return (
        sample_station_states,
        expected_preprocessed_old_df,
        expected_preprocessed_new_df,
    )


@pytest.fixture
def expected_results() -> pd.DataFrame:
    """Fixture to provide expected results for the active period method.

    Returns
    -------
    pd.DataFrame
        A DataFrame with expected bottleneck ratios for each station.
    """
    result = pd.DataFrame(
        [
            {"station": "station_0", "bottleneck_ratio": 14.3},
            {"station": "station_1", "bottleneck_ratio": 14.4},
            {"station": "station_2", "bottleneck_ratio": 16.8},
            {"station": "station_3", "bottleneck_ratio": 21.7},
            {"station": "station_4", "bottleneck_ratio": 18.4},
            {"station": "station_5", "bottleneck_ratio": 18.6},
            {"station": "station_6", "bottleneck_ratio": 17.8},
            {"station": "station_7", "bottleneck_ratio": 11.0},
            {"station": "station_8", "bottleneck_ratio": 13.4},
            {"station": "station_9", "bottleneck_ratio": 13.5},
        ]
    )
    return result


class TestActivePeriodMethod:
    """Test class for ActivePeriodMethod."""

    def test__preprocess_states(
        self,
        active_period_method_factory: ActivePeriodMethod,
        preprocess_states_data: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    ) -> None:
        """
        Verify that _preprocess_states removes consecutive duplicate statuses.
        Data is sorted only by timestamp.

        Parameters
        ----------
        active_period_method_factory : ActivePeriodMethod
            Factory function to create an instance of the active period method.
        preprocess_states_data : tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
            Tuple containing the sample station states DataFrame.
        """
        (
            sample_station_states,
            expected_preprocessed_old_df,
            expected_preprocessed_new_df,
        ) = preprocess_states_data

        # Instantiate the active period method (which calls _preprocess_states
        # during init)
        active_period_method = active_period_method_factory(
            station_states_df=sample_station_states
        )
        processed_df = active_period_method.station_states_df.reset_index(drop=True)

        # Select the correct expected DataFrame based on the implementation under test.
        expected_df = expected_preprocessed_new_df.reset_index(drop=True)
        pd.testing.assert_frame_equal(processed_df, expected_df)

    def test_active_period_method_previous_solution(
        self,
        active_period_method_factory: ActivePeriodMethod,
        expected_results: pd.DataFrame,
        station_states: callable,
    ):
        """Validate results of Active Period Method against previous solution.

        Parameters
        ----------
        active_period_method_factory : ActivePeriodMethod
            Factory function to create an instance of the active period method.
        expected_results : pd.DataFrame
            DataFrame containing expected bottleneck ratios for each station.
        station_states : callable
            Function to load station states data.
        """
        # Load the station states data
        active_period_method = active_period_method_factory(
            station_states_df=station_states(Path("tests/data/stations_states.csv"))
        )
        # Calculate momentary and average bottlenecks
        active_period_method.calculate_momentary_bottlenecks()
        bottleneck_df = active_period_method.calculate_average_bottlenecks()
        bottleneck_df = (
            bottleneck_df.groupby(by="station")
            .agg({"bottleneck_ratio": "sum"})
            .reset_index()
        )
        bottleneck_df["bottleneck_ratio"] = bottleneck_df["bottleneck_ratio"].round(1)
        print(bottleneck_df)
        # Check if the result matches the expected results
        pd.testing.assert_frame_equal(bottleneck_df, expected_results)

    @pytest.mark.parametrize(
        "stations, num_days, max_changes_per_day",
        [(10, 20, 5), (20, 40, 10), (40, 80, 20)],
    )
    def test__calculate_raw_bottlenecks_sanity(
        self, stations: int, num_days: int, max_changes_per_day: int
    ) -> None:
        """Validate the sanity of the calculated raw bottlenecks for randomly generated
        data, i.e.
        1. Raw bottlenecks are sorted by start time.

        Parameters
        ----------
        stations : int
            Number of stations to generate data for.
        num_days : int
            Number of days to generate data for.
        max_changes_per_day : int
            Maximum number of changes in status per day.
        """
        # Create data
        data = generate_mock_data(
            stations=stations,
            num_days=num_days,
            max_changes_per_day=max_changes_per_day,
        )

        # Calculate momentary bottlenecks
        active_period_method = ActivePeriodMethod(station_states_df=data)
        active_period_method._calculate_raw_bottlenecks()
        raw_bottlenecks = active_period_method.raw_bottlenecks
        df_raw = pd.DataFrame(raw_bottlenecks)

        # 1. Check that raw_bottlenecks are sorted by start time
        start_times = df_raw["start"]
        for i in range(1, len(start_times)):
            prev = start_times[i - 1]
            curr = start_times[i]
            if curr < prev:
                raise AssertionError(
                    f"raw_bottlenecks are not sorted by start time.\n"
                    f"First violation at index {i}: {prev} > {curr}.\n"
                    f"Whole list: {start_times.tolist()}"
                )

    @pytest.mark.parametrize(
        "stations, num_days, max_changes_per_day",
        [(10, 20, 5), (20, 40, 10), (40, 80, 20)],
    )
    def test_active_period_method_bottleneck_sanity(
        self, stations: int, num_days: int, max_changes_per_day: int
    ) -> None:
        """Validate the sanity of the calculated bottlenecks for randomly generated
        data, i.e. checks that:
        1. There are no length zero momentary bottlenecks
        2. There are no overlapping momentary sole bottlenecks on the same machine
        3. There are no overlapping momentary shifting bottlenecks on the same machine
        4. There are no overlaps between momentary sole bottlenecks and momentary
        shifting bottlenecks on the same machine. The only exception is that start time
        of one might be stop time of the other or vice versa, i.e. the overlap has
        length 0.
        5. There are no overlaps between momentary sole bottlenecks and momentary
        bottlenecks of other machines. The only exception is that start time of one
        might be stop time of the other or vice versa, i.e. the overlap has length 0.

        Parameters
        ----------
        stations : int
            Number of stations to generate data for.
        num_days : int
            Number of days to generate data for.
        max_changes_per_day : int
            Maximum number of changes in status per day.
        """
        # Create data
        data = generate_mock_data(
            stations=stations,
            num_days=num_days,
            max_changes_per_day=max_changes_per_day,
        )

        # Calculate momentary bottlenecks
        active_period_method = ActivePeriodMethod(station_states_df=data)
        active_period_method.calculate_momentary_bottlenecks()
        momentary_bottlenecks = active_period_method.momentary_bottlenecks

        # 1. No length zero momentary bottlenecks
        zero_length = momentary_bottlenecks[
            momentary_bottlenecks["start"] >= momentary_bottlenecks["stop"]
        ]
        assert zero_length.empty, (
            f"Found {len(zero_length)} bottlenecks with non-positive "
            f" duration:\n{zero_length}"
        )

        # 2. No overlapping momentary sole bottlenecks on the same machine
        sole = momentary_bottlenecks[momentary_bottlenecks["bottleneck_type"] == "sole"]
        for station, group in sole.groupby("station"):
            sorted_group = group.sort_values("start")
            overlaps = (sorted_group["stop"].shift() >= sorted_group["start"]).fillna(
                False
            )
            assert not overlaps.any(), f"Sole bottlenecks overlap on station {station}"

        # 3. No overlapping momentary shifting bottlenecks on the same machine
        shifting = momentary_bottlenecks[
            momentary_bottlenecks["bottleneck_type"] == "shifting"
        ]
        for station, group in shifting.groupby("station"):
            sorted_group = group.sort_values("start")
            overlaps = (sorted_group["stop"].shift() >= sorted_group["start"]).fillna(
                False
            )
            assert (
                not overlaps.any()
            ), f"Shifting bottlenecks overlap on station {station}."

        # 4. Sole and shifting bottlenecks may overlap only at start or stop time
        # on the same machine
        for station, group in momentary_bottlenecks.groupby("station"):
            sorted_group = group.sort_values("start")
            # Use fact that 2. and 3. already check for overlaps (including start/stop)
            # on same bottleneck type
            overlaps = (sorted_group["stop"].shift() > sorted_group["start"]).fillna(
                False
            )
            assert (
                not overlaps.any()
            ), f"Shifting and sole bottleneck overlap on station {station}."

        # 5. Sole bottlenecks may overlap with other machines bottlenecks only at start
        # or stop time
        sole = momentary_bottlenecks[momentary_bottlenecks["bottleneck_type"] == "sole"]

        for _, row1 in sole.iterrows():
            start1, stop1, station1 = row1["start"], row1["stop"], row1["station"]

            for _, row2 in momentary_bottlenecks.iterrows():
                station2 = row2["station"]
                if station2 == station1:
                    continue  # Skip same station

                start2, stop2 = row2["start"], row2["stop"]

                # Check if intervals overlap at all
                if start1 < stop2 and start2 < stop1:
                    # Compute the overlap
                    overlap_start = max(start1, start2)
                    overlap_stop = min(stop1, stop2)

                    # Overlap must have length 0
                    assert overlap_start == overlap_stop, (
                        f"Overlap between sole bottleneck on station {station1} "
                        f"and bottleneck on station {station2}."
                    )
