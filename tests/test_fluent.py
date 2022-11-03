"""
Tests that the fluent() method is adding the methods to the go.Figure class.
"""
from plasma import fluent
from plotly import graph_objects as go

fluent()


def test_all_methods_were_added():
    assert hasattr(go.Figure, "fix_marker_text")
    assert hasattr(go.Figure, "continuous_color")
    assert hasattr(go.Figure, "fix_facet_yaxes")
