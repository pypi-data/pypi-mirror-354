import concurrent.futures
import warnings
from typing import Optional

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects

from .machine import ActivePeriod, Machine
from .utils.natural_key import natural_key

ONLY_ONE_MACHINE_WARNING = (
    "Only one unique station in data given. "
    "For the Active Period Method to detect bottlenecks, "
    "at least two stations are required."
)


def warn_on_one_machine(apm: "ActivePeriodMethod") -> None:
    if apm.num_machines == 1:
        warnings.warn(message=ONLY_ONE_MACHINE_WARNING)


class ActivePeriodMethod:
    """Implementation of class for Active Period Method."""

    def __init__(
        self,
        station_states_df: pd.DataFrame,
    ) -> None:
        """
        Initialize Active Period Method object with a Pandas DataFrame

        Parameters
        ----------
        station_states_df : pd.DataFrame
            A DataFrame with at least three columns for the station
            name (named station), timestamp of recording the status
            change (named timestamp) and the status (named status).
        """
        self.station_states_df: pd.DataFrame = station_states_df
        # Check if the DataFrame has the required columns
        columns = station_states_df.columns
        for col in ["station", "timestamp", "status"]:
            if col not in columns:
                raise ValueError(f"Column '{col}' not found in DataFrame.")
        self.station_col = "station"
        self.timestamp_col = "timestamp"
        self.status_col = "status"
        self.start: pd.Timestamp | None = None
        self.stop: pd.Timestamp | None = None
        self.raw_bottlenecks: list[ActivePeriod] = []
        self.momentary_sole_bottlenecks: list[ActivePeriod] = []
        self.momentary_shifting_bottlenecks: list[ActivePeriod] = []
        self.momentary_bottlenecks: pd.DataFrame | None = None
        self.average_bottlenecks: pd.DataFrame | None = None
        self._preprocess_states()  # Preprocess the states
        self.unique_station: list[str] = sorted(
            list(self.station_states_df[self.station_col].unique()),
            key=natural_key,
        )
        self.num_machines: int = len(self.unique_station)
        warn_on_one_machine(self)  # Warn if only one machine is present
        self.machines: dict[str:Machine] = {
            key: Machine(key) for key in self.unique_station
        }
        self._calculate_periods()  # Update each machine's status history

        # Plotting variables
        self._avg_bottleneck_plot_title: str = "Average Bottlenecks"
        self._avg_bottleneck_xaxis_label: str = "Station"
        self._avg_bottleneck_yaxis_label: str = "Bottleneck Ratio [%]"
        self._momentary_bottleneck_plot_title: str = "Momentary Bottlenecks"
        self._momentary_bottleneck_xaxis_label: str = "Time"
        self._momentary_bottleneck_yaxis_label: str = "Station"
        self._sole_bottleneck_color: tuple[str] = ("#FF0000",)
        self._shifting_bottleneck_color: tuple[str] = ("#FFA500",)
        self._sole_bottleneck_pattern: str = "."
        self._shifting_bottleneck_pattern: str = "/"

    def calculate_momentary_bottlenecks(self) -> pd.DataFrame:
        """Calculates momentary bottlenecks based on raw bottlenecks by
        overlap comparison.

        Returns
        -------
        self.momentary_bottlenecks : pd.DataFrame
            DataFrame with momentary bottlenecks.
        """
        # Calculate raw bottlenecks
        self._calculate_raw_bottlenecks()
        # Differentiate between sole and shifting bottlenecks
        for idx in range(len(self.raw_bottlenecks) - 1):
            current_bottleneck = self.raw_bottlenecks[idx]
            next_bottleneck = self.raw_bottlenecks[idx + 1]
            # Fetch most recent shifting bottleneck if: present, same type as
            # current and with overlap
            if self.momentary_shifting_bottlenecks:
                last_shifting_bottleneck = self.momentary_shifting_bottlenecks[-1]
                if (
                    last_shifting_bottleneck.key != current_bottleneck.key
                    or last_shifting_bottleneck.stop < current_bottleneck.start
                ):
                    last_shifting_bottleneck = None
            else:
                last_shifting_bottleneck = None
            # Overlapping case: Two shifting bottlenecks and sole for
            # current bottleneck detection
            if current_bottleneck.stop > next_bottleneck.start:
                start_overlap = next_bottleneck.start
                stop_overlap = current_bottleneck.stop
                duration_overlap = stop_overlap - start_overlap
                # Check if overlapping with last shifting, if so combine
                if (
                    last_shifting_bottleneck is not None
                    and last_shifting_bottleneck.stop >= start_overlap
                ):
                    self.momentary_shifting_bottlenecks[-1] = ActivePeriod(
                        last_shifting_bottleneck.start,
                        stop_overlap,
                        stop_overlap - last_shifting_bottleneck.start,
                        last_shifting_bottleneck.key,
                    )
                # Otherwise add
                else:
                    self.momentary_shifting_bottlenecks.append(
                        ActivePeriod(
                            start_overlap,
                            stop_overlap,
                            duration_overlap,
                            current_bottleneck.key,
                        )
                    )
                # Always add shifting part of next one
                self.momentary_shifting_bottlenecks.append(
                    ActivePeriod(
                        start_overlap,
                        stop_overlap,
                        duration_overlap,
                        next_bottleneck.key,
                    )
                )
                # Sole bottleneck case
                # Do not overwrite last shifting bottleneck part if present
                if last_shifting_bottleneck is not None:
                    start_sole = last_shifting_bottleneck.stop
                else:
                    start_sole = current_bottleneck.start
                if start_overlap - start_sole > pd.Timedelta(0):
                    self.momentary_sole_bottlenecks.append(
                        ActivePeriod(
                            start_sole,
                            start_overlap,
                            start_overlap - start_sole,
                            current_bottleneck.key,
                        )
                    )
                # Add part for last loop
                if idx == len(self.raw_bottlenecks) - 2:
                    if next_bottleneck.stop - stop_overlap > pd.Timedelta(0):
                        self.momentary_sole_bottlenecks.append(
                            ActivePeriod(
                                stop_overlap,
                                next_bottleneck.stop,
                                next_bottleneck.stop - stop_overlap,
                                next_bottleneck.key,
                            )
                        )
            else:
                # Non-overlapping case: sole for current bottleneck_detection
                # Do not overwrite last shifting bottleneck part if present
                if last_shifting_bottleneck is not None:
                    start_sole = last_shifting_bottleneck.stop
                else:
                    start_sole = current_bottleneck.start
                if current_bottleneck.stop - start_sole > pd.Timedelta(0):
                    self.momentary_sole_bottlenecks.append(
                        ActivePeriod(
                            start_sole,
                            current_bottleneck.stop,
                            current_bottleneck.stop - start_sole,
                            current_bottleneck.key,
                        )
                    )
                # Add part for last loop
                if idx == len(self.raw_bottlenecks) - 2:
                    self.momentary_sole_bottlenecks.append(next_bottleneck)

        # Create DataFrames from momentary bottleneck data
        momentary_shifting_bottlenecks_df = pd.DataFrame(
            self.momentary_shifting_bottlenecks
        )
        momentary_shifting_bottlenecks_df["bottleneck_type"] = "shifting"
        momentary_sole_bottlenecks_df = pd.DataFrame(self.momentary_sole_bottlenecks)
        momentary_sole_bottlenecks_df["bottleneck_type"] = "sole"
        momentary_bottlenecks_df = pd.concat(
            [momentary_shifting_bottlenecks_df, momentary_sole_bottlenecks_df],
            ignore_index=True,
        )
        self.momentary_bottlenecks = momentary_bottlenecks_df.rename(
            columns={"key": "station"}
        )
        return self.momentary_bottlenecks

    def calculate_average_bottlenecks(self) -> pd.DataFrame:
        """Calculate average bottlenecks based on momentary bottlenecks.
        This is done by summation of bottleneck durations and division by the
        total observed period of the station.
        Note that non-pause times might differ per station.

        Returns
        -------
        average_bottlenecks_df : pd.DataFrame
            DataFrame with average bottlenecks.
        """
        avg_bottlenecks_df = (
            self.momentary_bottlenecks.groupby(["station", "bottleneck_type"])
            .agg({"duration": "sum"})
            .reset_index()
        )
        observed_time_df = pd.DataFrame(
            {"station": station_name, "observed_time": station.non_pause_total_time}
            for station_name, station in self.machines.items()
        )
        avg_bottlenecks_df = pd.merge(
            avg_bottlenecks_df, observed_time_df, on="station", how="outer"
        )
        avg_bottlenecks_df["bottleneck_ratio"] = (
            avg_bottlenecks_df["duration"] / avg_bottlenecks_df["observed_time"]
        )
        avg_bottlenecks_df["bottleneck_ratio"] = (
            avg_bottlenecks_df["bottleneck_ratio"] * 100
        )
        self.average_bottlenecks = avg_bottlenecks_df
        return avg_bottlenecks_df

    def visualize_momentary_bottlenecks(
        self,
        sole_color: Optional[str] = "#FF0000",
        shifting_color: Optional[str] = "#FFA500",
        sole_pattern: Optional[str] = ".",
        shifting_pattern: Optional[str] = "/",
        plotter: Optional[str] = "matplotlib",
    ) -> plt.Figure | plotly.graph_objects.Figure:
        """Visualize momentary bottlenecks in station Gantt with selected plotter

        Parameters
        ----------
        sole_color : str, optional
            Color for sole bottlenecks, by default "#FF0000".
        shifting_color : str, optional
                Color for shifting bottlenecks, by default "#FFA500".
        sole_pattern : str, optional
                Pattern for sole bottlenecks, by default ".".
        shifting_pattern : str, optional
                Pattern for shifting bottlenecks, by default "/".
        plotter : str, optional
            Plotter to use, options are "matplotlib" or "plotly", by default
            "matplotlib".
        """
        self._sole_bottleneck_color = sole_color
        self._shifting_bottleneck_color = shifting_color
        self._sole_bottleneck_pattern = sole_pattern
        self._shifting_bottleneck_pattern = shifting_pattern
        # Plotting depending on plotter
        if plotter == "matplotlib":
            return self._plot_momentary_bottleneck_with_matplotlib()
        elif plotter == "plotly":
            return self._plot_momentary_bottlenecks_with_plotly()
        else:
            raise ValueError("Invalid plotter specified. Use 'matplotlib' or 'plotly'.")

    def visualize_average_bottlenecks(
        self,
        sole_color: Optional[str] = "#FF0000",
        shifting_color: Optional[str] = "#FFA500",
        sole_pattern: Optional[str] = ".",
        shifting_pattern: Optional[str] = "/",
        plotter: Optional[str] = "matplotlib",
    ) -> plt.Figure | plotly.graph_objects.Figure:
        """Visualize average bottlenecks with selected plotter.

        Parameters
        ----------
        sole_color : str, optional
            Color for sole bottlenecks, by default "#FF0000".
        shifting_color : str, optional
            Color for shifting bottlenecks, by default "#FFA500".
        sole_pattern : str, optional
                Pattern for sole bottlenecks, by default ".".
        shifting_pattern : str, optional
                Pattern for shifting bottlenecks, by default "/".
        plotter : str, optional
                Plotter to use, options are "matplotlib" or "plotly", by default
                "matplotlib".
        """
        self._sole_bottleneck_color = sole_color
        self._shifting_bottleneck_color = shifting_color
        self._sole_bottleneck_pattern = sole_pattern
        self._shifting_bottleneck_pattern = shifting_pattern
        # Plotting depending on plotter
        if plotter == "matplotlib":
            return self._plot_avg_bottlenecks_with_matplotlib()
        elif plotter == "plotly":
            return self._plot_avg_bottlenecks_with_plotly()
        else:
            raise ValueError("Invalid plotter specified. Use 'matplotlib' or 'plotly'.")

    # Private methods
    def _preprocess_states(self) -> None:
        """
        Remove consecutive duplicate statuses per station and sort
        the DataFrame by timestamp.
        """
        # Sort by timestamp column
        df = self.station_states_df.sort_values(self.timestamp_col)
        # Identify rows where the status differs from the previous record
        # in each station group
        mask = df.groupby(self.station_col)[self.status_col].transform(
            lambda s: s != s.shift()
        )
        # Only keep those rows
        self.station_states_df = df[mask].reset_index(drop=True)

    def _calculate_periods(self) -> None:
        """
        Update each machine's status history by iterating
        over the preprocessed DataFrame.
        """
        for row in self.station_states_df.itertuples(index=False):
            station = getattr(row, self.station_col)
            timestamp = getattr(row, self.timestamp_col)
            status = getattr(row, self.status_col)
            self.machines[station].update_machine(timestamp, status)

    @staticmethod
    def _get_minimal_start(machine) -> pd.Timestamp:
        """Get minimal start time for a machine.

        Parameters
        ----------
        machine : Machine
            The machine object to get the minimal start time from.

        Returns
        -------
        pd.Timestamp
            The minimal start time of the machine.
        """
        return machine.get_minimal_start()

    @staticmethod
    def _get_maximal_stop(machine) -> pd.Timestamp:
        """Get maximal stop time for a machine.

        Parameters
        ----------
        machine : Machine
            The machine object to get the maximal stop time from.

        Returns
        -------
        pd.Timestamp
            The maximal stop time of the machine.
        """
        return machine.get_maximal_stop()

    def _calculate_start(self) -> None:
        """Calculates start as minimal start over all machines.
        Executes in parallel for all machines to speed up the process.
        Note: For empty machine history, None is returned.

        Raises
        ------
        ValueError
            If no start time is found in the data.
        """
        # Use ThreadPoolExecutor to parallelize the calculation
        with concurrent.futures.ThreadPoolExecutor() as executor:
            start_times = executor.map(
                ActivePeriodMethod._get_minimal_start,
                self.machines.values(),
            )
        # Filter out None values and get the minimum start time
        self.start = min(start_times, default=None)

        # Check if start time is None
        if self.start is None:
            raise ValueError("No start time found in data.")

    def _calculate_stop(self) -> None:
        """Calculates stop as maximal stop over all machines.
        Executes in parallel for all machines to speed up the process.
        Note: For empty machine history, None is returned.

        Raises
        ------
        ValueError
            If no stop time is found in the data.
        """
        # Use ThreadPoolExecutor to parallelize the calculation
        with concurrent.futures.ThreadPoolExecutor() as executor:
            end_times = executor.map(
                ActivePeriodMethod._get_maximal_stop,
                self.machines.values(),
            )
        # Filter out None values and get the maximum stop time
        self.stop = max(end_times, default=None)

        # Check if stop time is None
        if self.stop is None:
            raise ValueError("No stop time found in data.")

    def _calculate_raw_bottlenecks(self) -> None:
        """Calculates "raw" bottlenecks, i.e. without sole / shifting
        differentiation.
        """
        # Calculate start and stop
        self._calculate_start()
        self._calculate_stop()
        current_time = self.start
        while current_time < self.stop:
            # Begin with start time and loop until stop time is reached
            current_active_periods = {}
            for key, machine in self.machines.items():
                # Calculate current active periods
                active_period = machine.get_active_period(current_time)
                if active_period is not None:
                    current_active_periods[key] = active_period
            if len(current_active_periods) > 0:
                # Calculate current bottlenecks
                key_longest = None
                value_longest = pd.Timedelta(0)
                for key, value in current_active_periods.items():
                    if value.duration > value_longest:
                        key_longest = key
                        value_longest = value.duration
                        current_active_periods[key_longest] = ActivePeriod(
                            current_active_periods[key_longest].start,
                            current_active_periods[key_longest].stop,
                            current_active_periods[key_longest].duration,
                            key_longest,
                        )
                        current_bottlenecks = [current_active_periods[key_longest]]
                    elif value.duration == value_longest:
                        key_longest = key
                        value_longest = value.duration
                        current_active_periods[key_longest] = ActivePeriod(
                            current_active_periods[key_longest].start,
                            current_active_periods[key_longest].stop,
                            current_active_periods[key_longest].duration,
                            key_longest,
                        )
                        current_bottlenecks.append(current_active_periods[key_longest])
                # Sort current bottlenecks by start time
                current_bottlenecks.sort(key=lambda x: x.start)
                # Add current bottlenecks to raw bottlenecks
                self.raw_bottlenecks.extend(current_bottlenecks)
                # Update time as end of bottlenecks duration
                current_time = max(
                    current_bottleneck.stop
                    for current_bottleneck in current_bottlenecks
                )
            else:
                # Update time as next start of period
                previous_time = current_time
                current_time = min(
                    machine.get_next_time(previous_time)
                    for machine in self.machines.values()
                    if machine.get_next_time(previous_time) is not None
                )
                # Safeguard against infinite loop
                if current_time == previous_time:
                    break

    def _plot_momentary_bottleneck_with_matplotlib(self) -> plt.Figure:
        """Plot momentary bottlenecks using matplotlib.

        Returns
        -------
        plt.Figure
            Figure object containing the plot.
        """
        # Set y positions for each machine
        y_pos = {key: -i for i, key in enumerate(self.unique_station)}
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(15, 5))
        # Add momentary sole bottlenecks to the plot
        for active_period in self.momentary_sole_bottlenecks:
            ax.barh(
                y_pos[active_period.key],
                active_period.stop - active_period.start,
                left=active_period.start,
                color=self._sole_bottleneck_color,
                hatch=self._sole_bottleneck_pattern,
                edgecolor="black",
                label="Sole Bottleneck",
            )
        # Add momentary shifting bottlenecks to the plot
        for active_period in self.momentary_shifting_bottlenecks:
            ax.barh(
                y_pos[active_period.key],
                active_period.stop - active_period.start,
                left=active_period.start,
                color=self._shifting_bottleneck_color,
                hatch=self._shifting_bottleneck_pattern,
                edgecolor="black",
                label="Shifting Bottleneck",
            )
        # Axis settings
        ax.set_yticks(list(y_pos.values()))
        ax.set_yticklabels(list(y_pos.keys()))
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        plt.xticks(rotation=45)
        # Labels and title
        ax.set_xlabel(self._momentary_bottleneck_xaxis_label)
        ax.set_ylabel(self._momentary_bottleneck_yaxis_label)
        ax.set_title(self._momentary_bottleneck_plot_title)
        # Legend
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        fig.tight_layout()
        return fig

    def _plot_momentary_bottlenecks_with_plotly(self) -> plotly.graph_objects.Figure:
        """Plot momentary bottlenecks using plotly.

        Returns
        -------
        plotly.graph_objects.Figure
            Figure object containing the plot.
        """
        fig = px.timeline(
            self.momentary_bottlenecks,
            x_start="start",
            x_end="stop",
            y="station",
            color="bottleneck_type",
            color_discrete_map={
                "sole": self._sole_bottleneck_color,
                "shifting": self._shifting_bottleneck_color,
            },
            pattern_shape="bottleneck_type",
            pattern_shape_map={"sole": ".", "shifting": "/"},
        )
        fig.update_layout(
            title=dict(text=self._momentary_bottleneck_plot_title),
            xaxis=dict(title=dict(text=self._momentary_bottleneck_xaxis_label)),
            yaxis=dict(title=dict(text=self._momentary_bottleneck_yaxis_label)),
        )
        return fig

    def _plot_avg_bottlenecks_with_matplotlib(self) -> plt.Figure:
        """Plot average bottlenecks using matplotlib.

        Returns
        -------
        plt.Figure
            Figure object containing the plot.
        """
        df = self.average_bottlenecks

        # Pivot the data to get bottleneck_ratios in columns by type
        pivot_df = df.pivot(
            index="station", columns="bottleneck_type", values="bottleneck_ratio"
        ).fillna(0)

        stations = pivot_df.index.tolist()
        sole_ratios = pivot_df.get("sole", pd.Series(0, index=stations))
        shifting_ratios = pivot_df.get("shifting", pd.Series(0, index=stations))

        bar_width = 0.35
        n_stations = len(stations)
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(
            range(n_stations),
            sole_ratios,
            bar_width,
            label="Sole Bottleneck",
            color=self._sole_bottleneck_color,
            hatch=self._sole_bottleneck_pattern,
            edgecolor="black",
        )

        ax.bar(
            range(n_stations),
            shifting_ratios,
            bar_width,
            bottom=sole_ratios,
            label="Shifting Bottleneck",
            color=self._shifting_bottleneck_color,
            hatch=self._shifting_bottleneck_pattern,
            edgecolor="black",
        )

        ax.set_xticks(range(n_stations))
        ax.set_xticklabels(stations)
        ax.set_xlabel(self._avg_bottleneck_xaxis_label)
        ax.set_ylabel(self._avg_bottleneck_yaxis_label)
        ax.set_title(self._avg_bottleneck_plot_title)

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())

        fig.tight_layout()
        return fig

    def _plot_avg_bottlenecks_with_plotly(self) -> plotly.graph_objects.Figure:
        """Plot average bottlenecks using plotly.

        Returns
        -------
        plotly.graph_objects.Figure
            Figure object containing the plot.
        """
        df = self.average_bottlenecks
        df = df.sort_values(by="bottleneck_type", ascending=False)
        fig = px.bar(
            df,
            x="station",
            y="bottleneck_ratio",
            color="bottleneck_type",
            color_discrete_map={
                "sole": self._sole_bottleneck_color,
                "shifting": self._shifting_bottleneck_color,
            },
            pattern_shape="bottleneck_type",
            pattern_shape_map={"sole": ".", "shifting": "/"},
        )
        fig.update_layout(
            barmode="stack",
            title=dict(text=self._avg_bottleneck_plot_title),
            xaxis=dict(title=dict(text=self._avg_bottleneck_xaxis_label)),
            yaxis=dict(title=dict(text=self._avg_bottleneck_yaxis_label)),
        )
        fig.update_xaxes(type="category")
        fig.update_yaxes(ticksuffix="%")
        return fig
