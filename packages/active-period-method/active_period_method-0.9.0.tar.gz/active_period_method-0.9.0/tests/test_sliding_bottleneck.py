# ----------------------- DEFINE TEST DATA ------------------------------------
import pandas as pd
import pytest

START_S1 = "2023-01-01 08:10:00"
START_S2 = "2023-01-01 08:20:00"
START_S3 = "2023-01-01 08:30:00"

END_S1 = "2023-01-01 08:35:00"
END_S2 = "2023-01-01 08:47:00"
END_S3 = "2023-01-01 08:55:00"

PRE_SLIDING_BOTTLENECK_ENTRIES = [
    {"station": "S3", "timestamp": "2023-01-01 08:01:00", "status": 1},
    {"station": "S3", "timestamp": "2023-01-01 08:03:00", "status": 0},
    {"station": "S1", "timestamp": "2023-01-01 08:04:00", "status": 1},
    {"station": "S1", "timestamp": "2023-01-01 08:05:00", "status": 0},
    {"station": "S2", "timestamp": "2023-01-01 08:07:00", "status": 1},
    {"station": "S2", "timestamp": "2023-01-01 08:10:00", "status": 0},
]

SLIDING_BOTTLENECK_ENTRIES = [
    {"station": "S1", "timestamp": START_S1, "status": 1},
    {"station": "S3", "timestamp": "2023-01-01 08:09:00", "status": 1},
    {"station": "S2", "timestamp": "2023-01-01 08:13:00", "status": 1},
    {"station": "S2", "timestamp": "2023-01-01 08:16:00", "status": 0},
    {"station": "S3", "timestamp": "2023-01-01 08:16:00", "status": 0},
    {"station": "S1", "timestamp": "2023-01-01 08:17:00", "status": 1},
    {"station": "S2", "timestamp": START_S2, "status": 1},
    {"station": "S3", "timestamp": "2023-01-01 08:23:00", "status": 1},
    {"station": "S2", "timestamp": "2023-01-01 08:23:00", "status": 1},
    {"station": "S3", "timestamp": "2023-01-01 08:27:00", "status": 0},
    {"station": "S2", "timestamp": "2023-01-01 08:30:00", "status": 1},
    {"station": "S3", "timestamp": START_S3, "status": 1},
    {"station": "S1", "timestamp": END_S1, "status": 0},
    {"station": "S1", "timestamp": "2023-01-01 08:37:00", "status": 1},
    {"station": "S1", "timestamp": "2023-01-01 08:40:00", "status": 0},
    {"station": "S3", "timestamp": "2023-01-01 08:40:00", "status": 1},
    {"station": "S2", "timestamp": "2023-01-01 08:42:00", "status": 1},
    {"station": "S1", "timestamp": "2023-01-01 08:43:00", "status": 1},
    {"station": "S1", "timestamp": "2023-01-01 08:45:00", "status": 1},
    {"station": "S1", "timestamp": "2023-01-01 08:47:00", "status": 1},
    {"station": "S3", "timestamp": "2023-01-01 08:50:00", "status": 1},
    {"station": "S2", "timestamp": END_S2, "status": 0},
    {"station": "S1", "timestamp": "2023-01-01 08:50:00", "status": 0},
    {"station": "S2", "timestamp": "2023-01-01 08:50:00", "status": 1},
    {"station": "S1", "timestamp": "2023-01-01 08:51:00", "status": 1},
    {"station": "S1", "timestamp": "2023-01-01 08:53:00", "status": 0},
    {"station": "S2", "timestamp": "2023-01-01 08:53:00", "status": 0},
    {"station": "S3", "timestamp": END_S3, "status": 0},
]


# ----------------------- TEST IMPLEMENTATION ---------------------------------


class TestSlidingT5:
    """Test class for sliding bottlenecks in the active period method."""

    @pytest.fixture
    def df(
        self,
        active_period_method_factory: callable,
        station_states: callable,
    ) -> pd.DataFrame:
        """Calculate momentary bottlenecks for the test.

        Parameters
        ----------
        active_period_method_factory : callable
            Factory function to create an instance of the active period method.
        station_states : callable
            Function to generate station states DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame containing momentary bottlenecks.
        """
        apm = active_period_method_factory(
            station_states_df=station_states(
                PRE_SLIDING_BOTTLENECK_ENTRIES + SLIDING_BOTTLENECK_ENTRIES
            )
        )
        return apm.calculate_momentary_bottlenecks()

    @pytest.mark.parametrize(
        "station, start, end",
        [
            ("S1", START_S1, START_S2),
            ("S3", END_S2, END_S3),
        ],
    )
    def test_sole(
        self, df: pd.DataFrame, station: str, start: pd.Timestamp, end: pd.Timestamp
    ) -> None:
        """Tests if expected sole bottlenecks with correct start and stop values exist.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the bottleneck data.
        station : str
            The station for which to filter the data.
        start : pd.Timestamp
            Start time of the bottleneck.
        end : pd.Timestamp
            Stop time of the bottleneck.
        """
        sole_bottlenecks = df[
            (df["station"] == station) & (df["bottleneck_type"] == "sole")
        ]
        assert len(sole_bottlenecks) > 0, "Didn't find any sole bottlenecks in data."
        assert any(
            bottleneck["start"] == pd.Timestamp(start)
            and bottleneck["stop"] == pd.Timestamp(end)
            for _, bottleneck in sole_bottlenecks.iterrows()
        ), f"Didn't find any matching sole bottleneck for from {start} to {end}."

    def test_sole_s2(self, df: pd.DataFrame) -> None:
        """Test that no sole bottleneck exists for S2 after the start of S1.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the bottleneck data.
        """
        sole_bottlenecks = df[
            (df["station"] == "S2") & (df["bottleneck_type"] == "sole")
        ]

        # Filter according to start of the S1 active period
        sole_bottlenecks = sole_bottlenecks[
            sole_bottlenecks["start"] > pd.Timestamp(START_S1)
        ]

        # Assert no sole bottleneck
        assert len(sole_bottlenecks) == 0

    @pytest.mark.parametrize(
        "station, start, end",
        [
            ("S1", START_S2, END_S1),
            ("S2", START_S2, END_S2),
            ("S3", START_S3, END_S2),
        ],
    )
    def test_shifting(
        self, df: pd.DataFrame, station: str, start: str, end: str
    ) -> None:
        """Test a shifting bottleneck with correct start and stop values exist.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the bottleneck data.
        station : str
            The station for which to filter the data.
        start : pd.Timestamp
            Start time of the bottleneck.
        end : pd.Timestamp
            Stop time of the bottleneck.
        """
        shifting_bottlenecks = df[
            (df["station"] == station) & (df["bottleneck_type"] == "shifting")
        ]
        assert (
            len(shifting_bottlenecks) > 0
        ), "Didn't find any shifting bottlenecks in data."
        assert any(
            bottleneck["start"] == pd.Timestamp(start)
            and bottleneck["stop"] == pd.Timestamp(end)
            for _, bottleneck in shifting_bottlenecks.iterrows()
        ), f"Didn't find any matching sole bottleneck for from {start} to {end}."
