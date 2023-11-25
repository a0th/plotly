from plasma.methods import dual, yoy, continuous_color, single_line, fix_facet_labels
from plotly import graph_objects as go

setattr(go.Figure, "yoy", yoy)
setattr(go.Figure, "single_line", single_line)
setattr(go.Figure, "fix_facet_labels", fix_facet_labels)
setattr(go.Figure, "dual", dual)
setattr(go.Figure, "continuous_color", continuous_color)
