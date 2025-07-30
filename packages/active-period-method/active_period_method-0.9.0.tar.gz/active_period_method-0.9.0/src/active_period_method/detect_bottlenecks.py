from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects

from .active_period_method import ActivePeriodMethod


def detect_bottlenecks(
    station_states_df: pd.DataFrame,
    plotter: Optional[str] = None,  # "matplotlib", "plotly", or None
) -> (
    tuple[pd.DataFrame, pd.DataFrame]
    | tuple[
        pd.DataFrame,
        pd.DataFrame,
        plt.Figure | plotly.graph_objects.Figure,
        plt.Figure | plotly.graph_objects.Figure,
    ]
):
    """
    Run the Active Period Method (APM) on the provided station status DataFrame
    to detect bottlenecks. This function computes momentary and average bottlenecks
    and optionally generates plots. If plots are generated, either matplotlib or
    plotly can be used.

    Parameters:
    -----------
    station_states_df : pd.DataFrame
        DataFrame containing station status data.
    plotter : str, optional
        Specifies a plotter for visualization. Options are "matplotlib", "plotly",
        or None. Default is None, which means no plots will be generated.

    Returns:
    --------
    momentary_bottlenecks : pd.DataFrame
        DataFrame containing momentary bottlenecks.
    average_bottlenecks : pd.DataFrame
        DataFrame containing average bottlenecks.
    fig_momentary : plt.Figure or plotly.graph_objects.Figure, optional
        Plot object for momentary bottlenecks. Only returned if plotter is specified.
    fig_average : plt.Figure or plotly.graph_objects.Figure, optional
        Plot object for average bottlenecks. Only returned if plotter is specified.

    Examples
    --------
    >>> df = generate_mock_data()
    >>> mom, avg = detect_bottlenecks(df)

    >>> mom, avg, fig_mom, fig_avg = detect_bottlenecks(df, plotter="matplotlib")
    >>> fig_mom.show()
    >>> fig_avg.show()
    """
    # Initialize active period method and compute bottlenecks
    active_period_method = ActivePeriodMethod(station_states_df)
    momentary_bottlenecks = active_period_method.calculate_momentary_bottlenecks()
    average_bottlenecks = active_period_method.calculate_average_bottlenecks()

    # Generate plots if a plotter is specified
    if plotter is not None:
        # Generate plots based on the specified plotter
        fig_momentary = active_period_method.visualize_momentary_bottlenecks(
            plotter=plotter
        )
        fig_average = active_period_method.visualize_average_bottlenecks(
            plotter=plotter
        )
        return momentary_bottlenecks, average_bottlenecks, fig_momentary, fig_average
    else:
        return momentary_bottlenecks, average_bottlenecks
