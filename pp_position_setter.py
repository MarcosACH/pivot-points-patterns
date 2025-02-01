import pandas as pd


def set_pivot_point_position(data, offset=1e-5):
    """
    Sets pivot point positions.

    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame containing columns "is_pivot", "High", and "Low".
    offset : float, optional
        The offset to add/subtract to/from pivot points, by default 1e-5.

    Returns:
    --------
    pandas.DataFrame <br>
        The input DataFrame with an added "pointpos" column.
    """

    data["pointpos"] = pd.NA

    data.loc[data["is_pivot"] == 1, "pointpos"] = data["High"] + offset
    data.loc[data["is_pivot"] == 2, "pointpos"] = data["Low"] - offset

    return data
