from plasma import fix_marker_text
from plotly import graph_objects as go
import plotly.express as px
import pandas as pd
import pytest 

@pytest.fixture(scope='module')
def basic_figure_example() -> go.Figure:
    return px.line(pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6],
    }))

def test_fix_marker_text(basic_figure_example):
    fixed_fig_to_assert = basic_figure_example.fix_marker_text().to_dict()
    assert fixed_fig_to_assert['data'][0]['texttemplate'] == '%{text:.1f}'