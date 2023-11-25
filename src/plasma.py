import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

import pandas as pd
import plotly.express as px

from copy import deepcopy


def dual(f):
    first_chart = f.data[0]
    second_chart = f.data[1]
    return (
        make_subplots(specs=[[{"secondary_y": True}]])
        .add_trace(
            go.Scatter(x=first_chart.x, y=first_chart.y, name=first_chart.name),
            secondary_y=False,
        )
        .add_trace(
            go.Scatter(x=second_chart.x, y=second_chart.y, name=second_chart.name),
            secondary_y=True,
        )
        .update_yaxes(
            title_text=second_chart.name,
            secondary_y=True,
        )
        .update_yaxes(
            title_text=first_chart.name,
            secondary_y=False,
        )
        .update_layout(yaxis2=dict(showgrid=False, zeroline=False))
    )


def yoy(fig):
    fig.data[1].x = [z.replace(year=2020) for z in fig.data[1].x]
    fig.data[2].x = [z.replace(year=2020) for z in fig.data[2].x]
    return fig.update_xaxes(tickformat="%b %d")


def continuous_color(fig, colorscale: str = "Blues"):
    n_traces = len(fig.data)
    colors = px.colors.sample_colorscale(colorscale, n_traces)
    for index, color in enumerate(colors):
        fig.data[index]["line"]["color"] = color
    return fig


def fix_facet_labels(fig, **kwargs):
    fig = deepcopy(fig)
    return fig.for_each_annotation(
        lambda annotation: annotation.update(
            text=annotation.text.split("=")[1], **kwargs
        )
    )


def single_line(fig):
    _fig = deepcopy(fig)
    first_x = fig.data[0].x.tolist()
    first_y = fig.data[0].y.tolist()
    second_x = fig.data[1].x.tolist()
    second_y = fig.data[1].y.tolist()
    new_x = sorted(first_x + second_x)
    left_y = []

    right_y = []
    for x in new_x:
        if x in first_x:
            left_y.append(first_y[first_x.index(x)])
            right_y.append(None)
        else:
            left_y.append(None)
            right_y.append(second_y[second_x.index(x)])

    _fig.data[0].x = new_x
    _fig.data[0].y = left_y
    _fig.data[1].x = new_x
    _fig.data[1].y = right_y
    return _fig


setattr(go.Figure, "yoy", yoy)
setattr(go.Figure, "single_line", single_line)
setattr(go.Figure, "continuous_color", continuous_color)
setattr(go.Figure, "fix_facet_labels", fix_facet_labels)
setattr(go.Figure, "dual", dual)
