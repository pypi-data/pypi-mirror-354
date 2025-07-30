import pandas as pd
import pytest

from active_period_method.machine import ActivePeriod, Machine, Period


@pytest.fixture
def history_empty() -> list[Period]:
    """Fixture to provide an empty history for testing.

    Returns
    -------
    list[Period]
        An empty list representing the history of a machine.
    """
    return []


@pytest.fixture
def history_not_empty() -> list[Period]:
    """Fixture to provide a non-empty history for testing.

    Returns
    -------
    list[Period]
        A list of Period objects representing the history of a machine.
    """
    return [
        Period(
            pd.Timestamp("2025-02-20"),
            pd.Timestamp("2025-02-25"),
            pd.Timedelta(days=5),
            True,
        ),
        Period(
            pd.Timestamp("2025-02-25"),
            pd.Timestamp("2025-02-28"),
            pd.Timedelta(days=3),
            False,
        ),
        Period(
            pd.Timestamp("2025-02-28"),
            pd.Timestamp("2025-03-01"),
            pd.Timedelta(1),
            True,
        ),
        Period(
            pd.Timestamp("2025-03-01"),
            pd.Timestamp("2025-03-05"),
            pd.Timedelta(days=4),
            False,
        ),
        Period(
            pd.Timestamp("2025-03-05"),
            pd.Timestamp("2025-03-10"),
            pd.Timedelta(days=5),
            True,
        ),
    ]


@pytest.mark.parametrize("machine_class", [Machine])
class TestMachine:
    """Test class for common methods of all machine class subclasses."""

    def test__init__(self, machine_class: Machine) -> None:
        """Test the initialization of the Machine class.

        Parameters
        ----------
        machine_class : Machine
            The class to be tested, which should be a subclass of Machine.
        """
        machine = machine_class("Machine 1")
        assert (
            machine.name == "Machine 1"
        ), f"Expected name to be 'Machine 1', got {machine.name}"
        assert machine.start is None, "Expected start to be None"
        assert machine.stop is None, "Expected stop to be None"
        assert machine.status is None, "Expected status to be None"
        assert machine.duration is None, "Expected duration to be None"
        assert machine.non_pause_total_time == pd.Timedelta(
            0
        ), "Expected non_pause_total_time to be 0"
        assert machine.history == [], "Expected history to be an empty list"

    def test_set_name(self, machine_class: Machine) -> None:
        """Test the set_name method of the Machine class.

        Parameters
        ----------
        machine_class : Machine
                The class to be tested, which should be a subclass of Machine.
        """
        machine = machine_class("Machine 1")
        machine.set_name("Machine 2")
        assert (
            machine.name == "Machine 2"
        ), f"Expected name to be 'Machine 2', got {machine.name}"

    @pytest.mark.parametrize(
        ["current_time", "expected_duration"],
        [
            pytest.param(
                None,
                pd.Timedelta(days=8),
                id="current_time is None",
            ),
            pytest.param(
                pd.Timestamp("2025-02-25"),
                pd.Timedelta(days=5),
                id="current_time is 2025-02-25",
            ),
        ],
    )
    def test_calculate_duration(
        self,
        machine_class: Machine,
        current_time: pd.Timestamp,
        expected_duration: pd.Timedelta,
    ) -> None:
        """Test the calculate_duration method of the Machine class.

        Parameters
        ----------
        machine_class : Machine
            The class to be tested, which should be a subclass of Machine.
        current_time : pd.Timestamp
            The current time to be used for duration calculation.
        expected_duration : pd.Timedelta
            The expected duration to be calculated.
        """
        machine = machine_class("Machine 1")
        machine.start = pd.Timestamp("2025-02-20")
        machine.stop = pd.Timestamp("2025-02-28")
        machine.calculate_duration(current_time)
        assert (
            machine.duration == expected_duration
        ), f"Expected duration to be {expected_duration}, got {machine.duration}"

    @pytest.mark.parametrize(
        ["start", "stop", "duration", "status", "history"],
        [
            pytest.param(
                pd.Timestamp("2025-02-20"),
                pd.Timestamp("2025-02-25"),
                pd.Timedelta(5),
                True,
                pytest.lazy_fixture("history_empty"),
                id="empty history",
            ),
            pytest.param(
                pd.Timestamp("2025-02-20"),
                pd.Timestamp("2025-02-25"),
                pd.Timedelta(5),
                True,
                pytest.lazy_fixture("history_not_empty"),
                id="not empty history",
            ),
        ],
    )
    def test_update_history(
        self,
        machine_class: Machine,
        start: pd.Timestamp,
        stop: pd.Timestamp,
        duration: pd.Timedelta,
        status: int | bool,
        history: list[Period],
    ) -> None:
        """Test the update_history method of the Machine class.

        Parameters
        ----------
        machine_class : Machine
            The class to be tested, which should be a subclass of Machine.
        start : pd.Timestamp
            Start time of the period.
        stop : pd.Timestamp
            Stop time of the period.
        duration : pd.Timedelta
            Duration of the period.
        status : int | bool
            Status of the period.
        history : list[Period]
            The history of the machine.
        """
        # Create a machine instance with the provided history
        machine = machine_class("Machine 1")
        machine.history = history
        # First history update
        machine.start = start
        machine.stop = stop
        machine.duration = duration
        machine.status = status
        machine.update_history()
        expected_entry = Period(start, stop, duration, status)
        assert (
            machine.history[-1] == expected_entry
        ), f"Expected last history entry {expected_entry}, got {machine.history[-1]}"
        # Second history update
        machine.start = start + pd.Timedelta(days=1)
        machine.stop = stop + pd.Timedelta(days=2)
        machine.duration = duration + pd.Timedelta(days=1)
        machine.status = not status
        machine.update_history()
        expected_entry = Period(
            start + pd.Timedelta(days=1),
            stop + pd.Timedelta(days=2),
            duration + pd.Timedelta(days=1),
            not status,
        )
        # Check if the last entry in history matches the expected entry
        assert (
            machine.history[-1] == expected_entry
        ), f"Expected last history entry {expected_entry}, got {machine.history[-1]}"

    @pytest.mark.parametrize(
        ["history", "expected_minimal_start"],
        [
            pytest.param(
                pytest.lazy_fixture("history_empty"),
                None,
                id="empty history",
            ),
            pytest.param(
                pytest.lazy_fixture("history_not_empty"),
                pd.Timestamp("2025-02-20"),
                id="not empty history",
            ),
        ],
    )
    def test_get_minimal_start(
        self,
        machine_class: Machine,
        history: list[Period],
        expected_minimal_start: pd.Timestamp,
    ) -> None:
        """Test the get_minimal_start method of the Machine class.

        Parameters
        ----------
        machine_class : Machine
            The class to be tested, which should be a subclass of Machine.
        history : list[Period]
            The history of the machine.
        expected_minimal_start : pd.Timestamp
            The expected minimal start time.
        """
        machine = machine_class("Machine 1")
        machine.history = history
        assert (
            machine.get_minimal_start() == expected_minimal_start
        ), f"Exp. m. start {expected_minimal_start}, got {machine.get_minimal_start()}"

    @pytest.mark.parametrize(
        ["history", "expected_maximal_stop"],
        [
            pytest.param(
                pytest.lazy_fixture("history_empty"),
                None,
                id="empty history",
            ),
            pytest.param(
                pytest.lazy_fixture("history_not_empty"),
                pd.Timestamp("2025-03-05"),
                id="not empty history",
            ),
        ],
    )
    def test_get_maximal_stop(
        self,
        machine_class: Machine,
        history: list[Period],
        expected_maximal_stop: pd.Timestamp,
    ) -> None:
        """Test the get_maximal_stop method of the Machine class.

        Parameters
        ----------
        machine_class : Machine
            The class to be tested, which should be a subclass of Machine.
        history : list[Period]
            The history of the machine.
        expected_maximal_stop : pd.Timestamp
            The expected maximal stop time.
        """
        machine = machine_class("Machine 1")
        machine.history = history
        assert (
            machine.get_maximal_stop() == expected_maximal_stop
        ), f"Exp. m. stop {expected_maximal_stop}, got {machine.get_maximal_stop()}"

    @pytest.mark.parametrize(
        ["current_time", "expected_active_period"],
        [
            pytest.param(
                pd.Timestamp("2025-02-24"),
                ActivePeriod(
                    pd.Timestamp("2025-02-20"),
                    pd.Timestamp("2025-02-25"),
                    pd.Timedelta(days=5),
                    None,
                ),
                id="current_time 2025-02-24 is in AP",
            ),
            pytest.param(
                pd.Timestamp("2025-02-26"),
                None,
                id="current_time 2025-02-26 is not in AP",
            ),
            pytest.param(
                pd.Timestamp("2025-02-28"),
                ActivePeriod(
                    pd.Timestamp("2025-02-28"),
                    pd.Timestamp("2025-03-01"),
                    pd.Timedelta(1),
                    None,
                ),
                id="current_time 2025-02-28 is on left (included) boundary of AP",
            ),
            pytest.param(
                pd.Timestamp("2025-03-01"),
                None,
                id="current_time 2025-03-01 is on right (excluded) boundary of AP",
            ),
        ],
    )
    def test_get_active_period(
        self,
        machine_class: Machine,
        current_time: pd.Timestamp,
        expected_active_period: ActivePeriod,
        history_not_empty: list[Period],
    ):
        """Test the get_active_period method of the Machine class.

        Parameters
        ----------
        machine_class : Machine
            The class to be tested, which should be a subclass of Machine.
        current_time : pd.Timestamp
            The current time to be used for active period calculation.
        expected_active_period : ActivePeriod
            The expected active period.
        history_not_empty : list[Period]
            The history of the machine, which should not be empty.
        """
        machine = machine_class("Machine 1")
        machine.history = history_not_empty
        active_period = machine.get_active_period(current_time)
        assert (
            machine.get_active_period(current_time) == expected_active_period
        ), f"Exp. AP {expected_active_period}, got {active_period}"

    @pytest.mark.parametrize(
        ["current_time", "expected_next_time"],
        [
            pytest.param(
                pd.Timestamp("2025-02-24"),
                pd.Timestamp("2025-02-25"),
                id="current_time 2025-02-24 is in AP",
            ),
            pytest.param(
                pd.Timestamp("2025-02-26"),
                pd.Timestamp("2025-02-28"),
                id="current_time 2025-02-26 is not in AP",
            ),
            pytest.param(
                pd.Timestamp("2025-02-28"),
                pd.Timestamp("2025-03-01"),
                id="current_time 2025-02-28 is on left (included) boundary of AP",
            ),
            pytest.param(
                pd.Timestamp("2025-03-01"),
                pd.Timestamp("2025-03-05"),
                id="current_time 2025-03-01 is on right (excluded) boundary of AP",
            ),
            pytest.param(
                pd.Timestamp("2025-03-05"),
                None,
                id="current_time 2025-03-05 is in last period",
            ),
        ],
    )
    def test_get_next_time(
        self,
        machine_class: Machine,
        current_time: pd.Timestamp,
        expected_next_time: pd.Timestamp,
        history_not_empty: list[Period],
    ) -> None:
        """Test the get_next_time method of the Machine class.

        Parameters
        ----------
        machine_class : Machine
            The class to be tested, which should be a subclass of Machine.
        current_time : pd.Timestamp
            The current time to be used for next time calculation.
        expected_next_time : pd.Timestamp
            The expected next time.
        history_not_empty : list[Period]
            The history of the machine, which should not be empty.
        """
        machine = machine_class("Machine 1")
        machine.history = history_not_empty
        next_time = machine.get_next_time(current_time)
        assert (
            machine.get_next_time(current_time) == expected_next_time
        ), f"Exp. next time {expected_next_time}, got {next_time}"

    @pytest.mark.parametrize(
        ["start", "status", "history"],
        [
            pytest.param(
                pd.Timestamp("2025-02-20"),
                False,
                pytest.lazy_fixture("history_empty"),
                id="empty history",
            ),
            pytest.param(
                pd.Timestamp("2025-03-20"),
                True,
                pytest.lazy_fixture("history_not_empty"),
                id="not empty history",
            ),
        ],
    )
    def test_update_machine(
        self,
        machine_class: Machine,
        start: pd.Timestamp,
        status: str | int,
        history: list[Period],
    ) -> None:
        """Test the update_machine method of the Machine class.

        Parameters
        ----------
        machine_class : Machine
            The class to be tested, which should be a subclass of Machine.
        start : pd.Timestamp
            Start time of the machine.
        status : str | int
            Status of the machine.
        history : list[Period]
            History of the machine.
        """
        # Create a machine instance with the provided history
        machine = machine_class("Machine 1")
        machine.history = history
        if len(history) > 0:
            machine.start = history[-1].stop
            machine.status = not history[-1].status
        # Update the machine with the new start and status
        machine.update_machine(start, status)
        # Check if the machine's attributes match the expected values
        assert machine.start == start, f"Expected start {start}, got {machine.start}"
        assert (
            machine.status == status
        ), f"Expected status {status}, got {machine.status}"
        if len(history) == 0:
            assert machine.history == [], "Expected history to be an empty list"
        else:
            expected_last_entry = Period(
                history[-1].start,
                start,
                start - history[-1].start,
                not status,
            )
            assert (
                machine.history[-1] == expected_last_entry
            ), f"Exp. last hist. entry {expected_last_entry}, got {machine.history[-1]}"
            assert machine.non_pause_total_time == start - history[-1].start, (
                f"Exp. non_pause_total_time to be {start - history[-1].start}, "
                f"got {machine.non_pause_total_time}"
            )
