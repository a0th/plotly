import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

import pandas as pd
import plotly.express as px


def fluent():
    setattr(go.Figure, "fix_marker_text", fix_marker_text)
    setattr(go.Figure, "continuous_lines", continuous_lines)


def fix_marker_text(
    fig: go.Figure,
    marker_format: str = None,
    tick_format: str = None,
    panel_font_size: int = 12,
) -> go.Figure:
    if marker_format is None:
        marker_format = "{:.1f}"
    if tick_format is None:
        tick_format = "{:.1f}"
    marker_format = marker_format.replace("{:", "%{text:")

    return fig.update_traces(
        texttemplate=marker_format,
        textposition="top center",
        textfont=go.scatter.Textfont(size=panel_font_size),
    ).update_yaxes(tickformat=tick_format[2:-1])


def _is_between_zero_and_one(x: np.ndarray) -> bool:
    return (x >= 0).all() and (x <= 1).all()


def dual_axis_line(
    df,
    left_axis: str | list[str],
    right_axis: str | list[str],
    left_axis_title: str = None,
    right_axis_title: str = None,
) -> go.Figure:
    if isinstance(left_axis, str):
        left_axis = [left_axis]
    if isinstance(right_axis, str):
        right_axis = [right_axis]

    assert len(set(left_axis) - set(df.columns)) == 0
    assert len(set(right_axis) - set(df.columns)) == 0
    if left_axis_title is None:
        left_axis_title = _secondary_axis_title(left_axis)
    if right_axis_title is None:
        right_axis_title = _secondary_axis_title(right_axis)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for c in left_axis:
        fig = fig.add_trace(go.Scatter(x=df.index, y=df[c], name=c), secondary_y=False)
    for c in right_axis:
        fig = fig.add_trace(go.Scatter(x=df.index, y=df[c], name=c), secondary_y=True)

    return (
        fig.update_yaxes(title_text=left_axis_title, secondary_y=False)
        .update_yaxes(
            title_text=right_axis_title,
            secondary_y=True,
        )
        .update_layout(yaxis2=dict(showgrid=False, zeroline=False))
    )


def _secondary_axis_title(axis: str | list[str]) -> str:
    if isinstance(axis, str):
        return axis
    else:
        return "/".join(axis)


def overlay_yoy(df: pd.DataFrame, y: str) -> go.Figure:

    return (
        px.line(
            df.assign(_chart_date=lambda df: df.index.strftime("2020-%m-%d")),
            x="_chart_date",
            y=y,
            color="year",
        )
        .update_xaxes(tickformat="%b %d")
        .update_xaxes(title=df.index.name)
    )


def continuous_lines(fig, colorscale: str = "Blues"):
    n_traces = len(fig.data)
    colors = px.colors.sample_colorscale(colorscale, n_traces)
    for index, color in enumerate(colors):
        fig.data[index]["line"]["color"] = color
    return fig
