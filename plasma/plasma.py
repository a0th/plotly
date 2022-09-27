import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def overload_fig():
    setattr(go.Figure, "fix_labels", fix_labels)


def fix_labels(
    fig: go.Figure,
    panel_format: str = None,
    tick_format: str = None,
    panel_format_auto_percent: bool = True,
    tick_format_auto_percent: bool = True,
    panel_font_size: int = 12,
) -> go.Figure:
    if panel_format is None:
        panel_format = "{:.1f}"
    if tick_format is None:
        tick_format = "{:.1f}"
    panel_format = panel_format.replace("{:", "%{text:")
    tick_format = tick_format[1:-1]
    if panel_format_auto_percent and _is_between_zero_and_one(fig.data[0].text):
        panel_format = panel_format[:-2] + "%}"
    if tick_format_auto_percent and _is_between_zero_and_one(fig.data[0].y):
        tick_format = tick_format[:-2] + "%}"

    return fig.update_traces(
        texttemplate=panel_format,
        textposition="top center",
        textfont=go.scatter.Textfont(size=panel_font_size),
    ).update_yaxes(tickformat=".1%")


def _is_between_zero_and_one(x: np.ndarray) -> bool:
    return (x >= 0).all() and (x <= 1).all()


def plot_line_with_secondary_y(
    df,
    left_axis: str | list[str],
    right_axis: str | list[str],
    left_axis_title: str = None,
    right_axis_title: str = None,
) -> go.Figure:
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

    fig.update_layout(yaxis2=dict(showgrid=False)).update_yaxes(
        title_text=left_axis_title,
        secondary_y=False,
    ).update_yaxes(
        title_text=right_axis_title,
        secondary_y=True,
    )

    return fig


def _secondary_axis_title(axis: str | list[str]) -> str:
    if isinstance(axis, str):
        return axis
    else:
        return "/".join(axis)
