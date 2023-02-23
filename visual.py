import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import math

# initialize the app
app = dash.Dash(__name__)

# set up the layout
app.layout = html.Div([
    html.H1("Functions with Sliders"),
    html.Div([
        html.H2("Graph parameters"),
        html.Label("Y-min: "),
        dcc.Slider(id="Ymin-slider", min=-400, max=0, step=50, value=-200),
        html.Label("Y-max: "),
        dcc.Slider(id="Ymax-slider", min=0, max=400, step=50, value=200),
        dcc.Graph(id="graph1", style={"height": "500px"}),
        html.Div([
            html.Button('C-command +', id='c-plus-btn', n_clicks=0),
            html.Button('C-command -', id='c-minus-btn', n_clicks=0),
            html.Button('R-command +', id='r-plus-btn', n_clicks=0),
            html.Button('R-command -', id='r-minus-btn', n_clicks=0)
        ]),
        html.H3("Function 1: f(x) = A * (1 + B^(C(x-D)))"),
        html.Label("D: "),
        dcc.Slider(id="D-slider", min=-15, max=5, step=0.25, value=-8.5),
        html.Label("A: "),
        dcc.Slider(id="A-slider", min=0, max=10, step=0.1, value=2),
        html.Label("B: "),
        dcc.Slider(id="B-slider", min=0, max=10, step=0.1, value=2.7),
        html.Label("C: "),
        dcc.Slider(id="C-slider", min=0, max=10, step=0.1, value=2),
        html.H3("Function 2: f(x) = E * (1 + F^(G(x-H)))"),
        html.Label("H: "),
        dcc.Slider(id="H-slider", min=-5, max=15, step=0.25, value=8.5),
        html.Label("E: "),
        dcc.Slider(id="E-slider", min=0, max=10, step=0.1, value=2),
        html.Label("F: "),
        dcc.Slider(id="F-slider", min=0, max=10, step=0.1, value=2.7),
        html.Label("G: "),
        dcc.Slider(id="G-slider", min=0, max=10, step=0.1, value=2)
    ])
])

def find_x(A, B, C, D, E, F, G, H):

    # Use a loop to check values of x until f(x) is close enough to 0.
    x = D  # Starting point
    true = True
    while true:
        x += 0.00001  # Increment x by 0.1 (you can adjust this as needed)
        tmp = 0.000001 * A * (1 + math.pow(B, C * (x - D))) - 0.000001 * E * (1 + math.pow(F, -G * (x - H)))
        if abs(tmp) <= 1e-2:
            true = False
        if x > H:
            true = False
    x = x
    return round(x,2)


# set up the callback for the first graph
@app.callback(
    [Output("graph1", "figure"), Output("H-slider", "value"), Output("D-slider", "value")],
    [Input("A-slider", "value"), Input("B-slider", "value"), Input("C-slider", "value"), Input("D-slider", "value"),
     Input("E-slider", "value"), Input("F-slider", "value"), Input("G-slider", "value"), Input("H-slider", "value"),
     Input("Ymin-slider", "value"), Input("Ymax-slider", "value"),
     Input("c-plus-btn", "n_clicks"), Input("c-minus-btn", "n_clicks"), Input("r-plus-btn", "n_clicks"),
     Input("r-minus-btn", "n_clicks")]
)

def update_graph(A, B, C, D, E, F, G, H, ymin, ymax, c_plus, c_minus, r_plus, r_minus):
    # Update H-slider and D-slider based on button clicks
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "c-plus-btn":
            H = H + 0.25
            D = D - 0.25
        elif button_id == "c-minus-btn":
            H = H - 0.25
            D = D + 0.25
        elif button_id == "r-plus-btn":
            H = H + 0.25
            D = D + 0.25
        elif button_id == "r-minus-btn":
            H = H - 0.25
            D = D - 0.25

    x = np.linspace(-10, 10, 10000)
    y1 = 0.000001 * A * (1 + B ** (C * (x - D)))
    y2 = -0.000001 * (E * (1 + F ** (-G * (x - H))))
    y_sum = y1 + y2

    # Evaluate y_sum when x = 0
    y_sum_at_x0 = 0.000001 * A * (1 + B ** (C * (-D))) - 0.000001 * (E * (1 + F ** (-G * (-H))))

    RC = find_x(A, B, C, D, E, F, G, H)
    k = 0
    if abs(RC) > 0:
        k = round((y_sum_at_x0 / -RC), 2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_sum, mode='lines', name='sum'))
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='AG'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='ANT'))
    fig.add_shape(
        # Line Vertical
        dict(
            type='line',
            yref='paper', y0=0, y1=1,
            xref='x', x0=0, x1=0,
            line=dict(color='black', width=2)
        )
    )
    fig.add_shape(
        # Horizontal line
        dict(
            type='line',
            xref='x', yref='y',
            x0=np.min(x), y0=y_sum_at_x0,
            x1=np.max(x), y1=y_sum_at_x0,
            line=dict(color='black', width=1, dash='dash')
        ))

    fig.update_layout(
        xaxis_title='Reference coordinate',
        yaxis_title='Force',
        title='Plot EPH. Force: ' + str(round(y_sum_at_x0, 2)) + ',  RC = ' + str(RC) + ',  k = ' + str(k),
        yaxis=dict(range=[ymin, ymax])
    )

    return fig, H, D


if __name__ == "__main__":
    app.run_server(debug=True)
