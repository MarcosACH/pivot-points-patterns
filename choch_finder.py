import numpy as np
import pandas as pd


def find_choch_pattern(data, bullish=True, bearish=True):
    """
    Identifies Change of Character (CHoCH) patterns in a dataset and marks 
    breakout points in a "pattern" column.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing the market data with at least the following columns:
        - "is_pivot": Specifies pivot points (1 for high, 2 for low, 0 for none).
        - "High": High prices of the candles.
        - "Low": Low prices of the candles.
        - "Close": Closing prices of the candles.
    bullish : bool, optional (default=True)
        If True, the function looks for bullish CHoCH patterns.
    bearish : bool, optional (default=True)
        If True, the function looks for bearish CHoCH patterns.

    Returns:
    --------
    pandas.DataFrame <br>
        The input DataFrame with an additional column "pattern":

        - 1 indicates a bullish CHoCH pattern.
        - -1 indicates a bearish CHoCH pattern.
        - 0 indicates no pattern.

    Pattern Logic:
    --------------
    A ChoCH pattern is defined using six consecutive pivot points:
    - For a bullish pattern:
        1. Pivot sequence: High (1), Low (2), High (1), Low (2), High (1), Low (2).
        2. Price structure:
           - High 1 > Low 2.
           - High 3 > Low 2 and High 3 < High 1.
           - Low 4 < Low 2.
           - High 5 > Low 4 and High 5 < High 3.
           - Low 6 < High 5 and Low 6 > Low 4.
        3. The breakout occurs when the close price rises above High 5.

    - For a bearish pattern:
        1. Pivot sequence: Low (2), High (1), Low (2), High (1), Low (2), High (1).
        2. Price structure:
           - Low 1 < High 2.
           - Low 3 < High 2 and Low 3 > Low 1.
           - High 4 > High 2.
           - Low 5 < High 4 and Low 5 > Low 3.
           - High 6 > Low 5 and High 6 < High 4.
        3. The breakout occurs when the close price falls below Low 5.
    """

    highs = data["High"].to_numpy()
    lows = data["Low"].to_numpy()
    closes = data["Close"].to_numpy()
    is_pivot = data["is_pivot"].to_numpy()

    pivot_indices = np.where((is_pivot == 1) | (is_pivot == 2))[0]

    patterns = np.zeros(len(data), dtype=int)

    for i in range(len(pivot_indices) - 5):
        idx1, idx2, idx3, idx4, idx5, idx6 = pivot_indices[i:i+6]
        pivot_types = is_pivot[[idx1, idx2, idx3, idx4, idx5, idx6]]

        if bullish and np.array_equal(pivot_types, [1, 2, 1, 2, 1, 2]):
            p1, p3, p5 = highs[[idx1, idx3, idx5]]
            p2, p4, p6 = lows[[idx2, idx4, idx6]]

            if (
                p1 > p2 and
                p3 > p2 and p3 < p1 and
                p4 < p2 and
                p5 > p4 and p5 < p3 and
                p6 < p5 and p6 > p4
            ):
                breakout_idx = np.where(closes[idx6:] > p5)[0]
                if breakout_idx.size > 0:
                    patterns[idx6 + breakout_idx[0]] = 1

        if bearish and np.array_equal(pivot_types, [2, 1, 2, 1, 2, 1]):
            p1, p3, p5 = lows[[idx1, idx3, idx5]]
            p2, p4, p6 = highs[[idx2, idx4, idx6]]

            if (
                p1 < p2 and
                p3 < p2 and p3 > p1 and
                p4 > p2 and
                p5 < p4 and p5 > p3 and
                p6 > p5 and p6 < p4
            ):
                breakout_idx = np.where(closes[idx6:] < p5)[0]
                if breakout_idx.size > 0:
                    patterns[idx6 + breakout_idx[0]] = -1

    data["pattern"] = patterns
    return data
