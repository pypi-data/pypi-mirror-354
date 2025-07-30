import dataclasses
from typing import Optional

import pandas as pd


@dataclasses.dataclass
class Period:
    """Class to represent a period with start, stop, duration and status."""

    start: pd.Timestamp
    stop: pd.Timestamp
    duration: pd.Timedelta
    status: int | bool


@dataclasses.dataclass
class ActivePeriod:
    """Class to represent an active period with start, stop, duration and key."""

    start: pd.Timestamp
    stop: pd.Timestamp
    duration: pd.Timedelta
    key: str | None


class Machine:
    """Implementation of class to handle machines for active period method."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.status: bool | None = None
        self.start: float | None = None
        self.stop: float | None = None
        self.duration: float | None = None
        self.non_pause_total_time: pd.Timedelta = pd.Timedelta(0)
        self.history: list[Period] = []
        self.duration: pd.Timedelta | None = None
        # Tracking attributes for last get_active_period call
        self._last_current_time: pd.Timestamp = pd.Timestamp.min
        self._last_history_index: int = 0

    # Puplic methods
    def set_name(self, name: str) -> None:
        self.name = name

    def calculate_duration(self, current_time: Optional[float] = None):
        """Calculates timespan from last start to current time or stop
        and sets it as duration.

        Parameters
        ----------
        current_time : Optional[float], optional
            Current_time to compare with.
        """
        if current_time is None:
            # use stop if no current time is givn
            current_time = self.stop
        self.duration = current_time - self.start

    def update_history(self) -> None:
        """Saves last period to machines history."""
        self.history.append(Period(self.start, self.stop, self.duration, self.status))

    def update_machine(self, start: pd.Timestamp, status: int) -> None:
        """Update machine status state based on start and status and save
        previous period to machines history.

        Parameters
        ----------
        start : float
            Start of next period.
        status : int
            Status of next period. Must be different from current one.

        Raises
        ------
        ValueError
            If new status is current status.
        ValueError
            If new start is not greater than old start.
        ValueError
            If new start is old start with same state.
        ValueError
            If new start is old start.
        """
        if (self.start is None) and (self.stop is None):
            # initial update
            self.start = start
            self.status = status
        else:
            # update with given previous period
            if self.status == status:
                raise ValueError("New status is current status!")
            if self.start > start:
                raise ValueError("New start not greater than old start!")
            if self.start == start:
                if self.status == status:
                    raise ValueError("New start is old start with same state!")
                else:
                    raise ValueError("New start is old start!")
            # calculate previous period and update history
            self.stop = start
            self.calculate_duration()
            self.update_history()
            self.non_pause_total_time += self.stop - self.start
            # start new period
            self.start = start
            self.status = status

    def get_active_period(self, current_time: pd.Timestamp) -> Period | None:
        """Returns the active period in which current_time falls.
        None if not an active period.
        Can efficiently search for active period if called in increasing order.

        Parameters
        ----------
        current_time : float
            Current reference time.

        Returns
        -------
        ActivePeriod
            Current active period with properties start, stop, duration and key.
            None if none exists.
        """
        # If current time has decreased, reset tracking attributes
        if current_time < self._last_current_time:
            self._rest_current_time_tracking()
        active_period = None
        # Iterate over history from last index
        for idx, period in enumerate(self.history[self._last_history_index :]):
            if (period.start <= current_time) and (period.stop > current_time):
                if period.status == 1:
                    active_period = ActivePeriod(
                        period.start, period.stop, period.duration, None
                    )
                # Update tracking attributes
                self._last_history_index += idx
                self._last_current_time = current_time
                break  # Stop once curren_time is in interval
        return active_period

    def get_minimal_start(self) -> pd.Timestamp | None:
        """Returns the start time of the first period in history.

        Returns
        -------
        pd.Timestamp | None
            Start time of the first period in history or None if history is empty.
        """
        if len(self.history) > 0:
            return self.history[0].start
        else:
            return None

    def get_maximal_stop(self) -> pd.Timestamp | None:
        """Returns the stop time of the last period in history.
        To avoid difficulties with calculating the duration of the last period,
        in the active period method, the start time of the last period is returned.

        Returns
        -------
        pd.Timestamp | None
            Start time of the last period in history or None if history is empty.
        """
        if len(self.history) > 0:
            return self.history[-1].start
        else:
            return None

    def get_next_time(self, current_time: pd.Timestamp) -> pd.Timestamp:
        """Returns the start time of the next period after the period in
        which current_time is.
        Can efficiently return start of next period if called in increasing order.

        Parameters
        ----------
        current_time : float
            Current reference time.

        Returns
        -------
        next_time : float
            Start of next period.
        """
        # If current time has decreased, reset tracking attributes
        if current_time < self._last_current_time:
            self._rest_current_time_tracking()
        next_time = None
        # Scan from the last known index forward
        for idx, period in enumerate(self.history[self._last_history_index :]):
            if period.start > current_time:
                next_time = period.start
                # Update the absolute index so next call can skip ahead
                self._last_history_index += idx
                break

        return next_time

    # Private methods
    def _rest_current_time_tracking(self) -> None:
        """Reset tracking attributes for last get_active_period call."""
        self._last_current_time = float("-inf")
        self._last_history_index = 0
