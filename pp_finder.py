import numpy as np
import pandas as pd


def find_pivot_points(data, window=17):
    """
    Identifies pivot points in the market data and marks them in a new column.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing market data with at least the following columns:
        - "High": High prices of the candles.
        - "Low": Low prices of the candles.
    window : int, optional (default=17)
        The number of periods to consider for identifying pivot points.
        - A pivot high is defined as the maximum "High" within the specified window.
        - A pivot low is defined as the minimum "Low" within the specified window.

    Returns:
    --------
    pandas.DataFrame <br>
        The input DataFrame with an additional column "is_pivot":

        - 1 indicates a pivot high.
        - 2 indicates a pivot low.
        - 0 indicates no pivot.

    Notes:
    ------
    - The `window` parameter should be an odd number to ensure symmetry around the center point.
    - Pivot points are assigned to the middle of the rolling window.
    """

    is_max = data["High"] == data["High"].rolling(
        window=window, center=True).max()
    is_min = data["Low"] == data["Low"].rolling(
        window=window, center=True).min()

    data["is_pivot"] = np.where(is_max, 1, np.where(is_min, 2, 0))

    return data
