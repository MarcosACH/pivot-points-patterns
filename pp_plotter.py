from pp_position_setter import set_pivot_point_position
import plotly.graph_objects as go
import pandas as pd


def plot_pivot_points(data):
    data = set_pivot_point_position(data)

    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data["Open"],
                                         high=data["High"],
                                         low=data["Low"],
                                         close=data["Close"],
                                         name="Candlesticks")])

    fig.add_scatter(x=data.index, y=data["pointpos"], mode="markers",
                    marker=dict(size=5, color="MediumPurple"),
                    name="Pivot")

    fig.update_layout(title="Candlestick Chart with Pivot Points",
                      xaxis_title="Time",
                      yaxis_title="Price",
                      template="plotly_dark",
                      height=900)
    fig.show()
