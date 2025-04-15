import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import pandas as pd
from urllib.request import urlopen
import shapely.geometry
import numpy as np
import json


def map():
    """ """
    fig = go.Figure()

    fig.add_trace(
        go.Scattermap(
            lon=[
                -122.3,
                -123.5,
                -121.8,
                -104.99,
                -87.62,
                -95.36,
                -90.05,
                -112.07,
                -71.06,
                -80.19,
            ],
            lat=[
                47.6,
                46.9,
                48.1,
                39.74,
                41.88,
                29.76,
                35.15,
                33.45,
                42.36,
                25.76,
            ],
            mode="markers",
            marker=dict(size=10, color="blue"),
            text=[
                "Seattle",
                "Portland",
                "Bellingham",
                "Denver",
                "Chicago",
                "Houston",
                "Memphis",
                "Phoenix",
                "Boston",
                "Miami",
            ],
        )
    )
    fig.update_layout(
        margin=dict(l=5, r=0, t=10, b=5),
        map_bounds={"west": -130, "east": -63.5, "south": 24.0, "north": 53.0},
    )
    return fig
