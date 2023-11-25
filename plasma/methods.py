from collections import namedtuple
from copy import deepcopy

import plotly.graph_objects as go
from plasma.colormap import get_color
from plotly.subplots import make_subplots


def dual(fig: go.Figure) -> go.Figure:
    """Make a dual y-axis plot from a plotly figure with two traces."""
    first_chart = fig.data[0]
    try:
        second_chart = fig.data[1]
    except IndexError as e:
        raise ValueError("Figure must have at least two traces to use dual()") from e
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
        .update_layout(yaxis2={"showgrid": False, "zeroline": False})
    )


def yoy(fig: go.Figure) -> go.Figure:
    """Make a year-over-year plot."""
    fig = deepcopy(fig)
    for trace in fig.data:
        trace.x = [date_index.replace(year=2020) for date_index in trace.x]
    return fig.update_xaxes(tickformat="%b %d")


def continuous_color(fig, colorscale: str = "Plotly"):
    color_name = fig.layout.legend.title.text
    color_values = []
    for data in fig.data:
        for hover_window_line_to_parse in data.hovertemplate.split("<br>"):
            name, value = hover_window_line_to_parse.split("=")
            if name == color_name:
                color_values.append(float(value))
    min_value = min(color_values)
    max_value = max(color_values)
    if len(color_values) == 1:
        normalized_color_values = [0.5]
    else:
        normalized_color_values = [
            (x - min_value) / (max_value - min_value) for x in color_values
        ]
    fig = deepcopy(fig)
    colors = [get_color(colorscale, x) for x in normalized_color_values]
    for data, color in zip(fig.data, colors):
        data["line"]["color"] = color
    return fig


def fix_facet_labels(fig, **kwargs):
    fig = deepcopy(fig)
    return fig.for_each_annotation(
        lambda annotation: annotation.update(
            text=annotation.text.split("=")[1], **kwargs
        )
    )


def single_line(fig):
    fig = deepcopy(fig)
    ChartData = namedtuple("ChartData", ["x", "y", "trace_id"])
    n_traces = len(fig.data)
    all_tuples: ChartData = []
    for trace_id, trace in enumerate(fig.data):
        for x, y in zip(trace.x, trace.y):
            all_tuples.append(ChartData(x, y, trace_id))
    all_tuples.sort(key=lambda tup: tup.x)
    new_x_array = [x for x, _, _ in all_tuples]
    new_y_arrays = [[] for _ in range(n_traces)]
    for tup in all_tuples:
        for current_trace_id in range(n_traces):
            if tup.trace_id == current_trace_id:
                new_y_arrays[current_trace_id].append(tup.y)
            else:
                new_y_arrays[current_trace_id].append(None)

    for trace_id, trace in enumerate(fig.data):
        trace.x = new_x_array
        trace.y = new_y_arrays[trace_id]

    return fig
