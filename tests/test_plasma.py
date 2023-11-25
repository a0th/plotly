import pandas as pd
import plotly.express as px
import plasma
from datetime import datetime


def test_dual():
    actual = (
        pd.DataFrame(
            {
                "x": [1, 2, 3, 4],
                "y1": [1, None, 2, 3],
                "y2": [9, None, 9, 10],
            }
        )
        .pipe(
            px.line,
            x="x",
            y=["y1", "y2"],
        )
        .dual()
        .to_dict()["layout"]["yaxis2"]
    )

    assert actual == {
        "anchor": "x",
        "overlaying": "y",
        "side": "right",
        "title": {"text": "y2"},
        "showgrid": False,
        "zeroline": False,
    }


def test_yoy():
    actual_x_axis = (
        pd.DataFrame(
            {
                "x": [pd.Timestamp("2023-01-01"), pd.Timestamp("2024-01-01")],
                "y": [0, 2],
            }
        )
        .pipe(px.line, x="x", y="y")
        .yoy()
        .data[0]["x"]
    )
    assert actual_x_axis == (datetime(2020, 1, 1), datetime(2020, 1, 1))
