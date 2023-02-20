import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# initialize the app
app = dash.Dash(__name__)

# set up the layout
app.layout = html.Div([
    html.H1("Functions with Sliders"),
    html.Div([
        html.H2("Graph parameters"),
        html.Label("Y-min: "),
        dcc.Slider(id="Ymin-slider", min=-2000, max=0, step=100, value=-1000),
        html.Label("Y-max: "),
        dcc.Slider(id="Ymax-slider", min=0, max=2000, step=100, value=1000),
        dcc.Graph(id="graph1", style={"height": "500px"}),
        html.H3("Function 1: f(x) = A * (1 + B^(C(x-D)))"),
        html.Label("A: "),
        dcc.Slider(id="A-slider", min=0, max=10, step=0.1, value=2),
        html.Label("B: "),
        dcc.Slider(id="B-slider", min=0, max=10, step=0.1, value=2.7),
        html.Label("C: "),
        dcc.Slider(id="C-slider", min=0, max=10, step=0.1, value=2),
        html.Label("D: "),
        dcc.Slider(id="D-slider", min=-10, max=10, step=0.1, value=-5),
        html.H3("Function 2: f(x) = E * (1 + F^(G(x-H)))"),
        html.Label("E: "),
        dcc.Slider(id="E-slider", min=0, max=10, step=0.1, value=2),
        html.Label("F: "),
        dcc.Slider(id="F-slider", min=0, max=10, step=0.1, value=2.7),
        html.Label("G: "),
        dcc.Slider(id="G-slider", min=0, max=10, step=0.1, value=2.5),
        html.Label("H: "),
        dcc.Slider(id="H-slider", min=-10, max=10, step=0.1, value=5)
    ])
])

# set up the callback for the first graph
@app.callback(
    Output("graph1", "figure"),
    [Input("A-slider", "value"), Input("B-slider", "value"), Input("C-slider", "value"), Input("D-slider", "value"),
     Input("E-slider", "value"), Input("F-slider", "value"), Input("G-slider", "value"), Input("H-slider", "value"),
     Input("Ymin-slider", "value"),Input("Ymax-slider", "value")]
)
def update_graph(A, B, C, D, E, F, G, H, ymin, ymax):
    x = np.linspace(-10, 10, 100)
    y1 = 0.001*A * (1 + B**(C*(x-D)))
    y2 = -0.001*(E * (1 + F**(-G*(x-H))))
    y_sum = y1 + y2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_sum, mode='lines', name='sum'))
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='AG'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='ANT'))


    fig.update_layout(
        xaxis_title='Muscle length',
        yaxis_title='Force',
        title='Plot EPH',
        yaxis=dict(range=[ymin, ymax])
    )
    
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
