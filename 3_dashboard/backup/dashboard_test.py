import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objs as go

# Initialisiere die Dash App
app = dash.Dash(__name__)
app.title = "Simulation of variance-aware algorithms for Stochastic Bandit Problems"

# Dummy-Plot Funktion
def create_dummy_plot(title):
    return dcc.Graph(
        figure={
            'data': [
                go.Scatter(x=[1, 2, 3], y=[4, 1, 2], mode='lines+markers')
            ],
            'layout': go.Layout(
                title=title,
                margin={'l': 30, 'r': 10, 'b': 30, 't': 40},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#2C2C2C'}
            )
        }
    )

# Layout der App
app.layout = html.Div(
    style={'backgroundColor': 'white', 'color': '#2C2C2C', 'font-family': 'Arial, sans-serif'},
    children=[
        html.Div(
            style={'textAlign': 'center', 'padding': '20px'},
            children=[
                html.H1("Simulation of variance-aware Algorithms for Stochastic Bandit Problems")
            ]
        ),
        html.Div(
            style={'display': 'flex'},
            children=[
                # Linke Navigationsleiste
                html.Div(
                    style={'flex': '1', 'padding': '20px', 'backgroundColor': 'white'},
                    children=[
                        html.H2("Einstellungen"),
                        html.Div(
                            children=[
                                html.Label('Verteilung der Arme'),
                                dcc.Dropdown(
                                    id='arm_distribution',
                                    options=[
                                        {'label': '2 Arme mit jeweils bernoulliverteilten Rewards mit mean [0.9, 0.8]', 'value': 'dist1'},
                                        {'label': '2 Arme mit jeweils bernoulliverteilten Rewards mit mean [0.9, 0.895]', 'value': 'dist2'},
                                        {'label': '2 Arme mit jeweils bernoulliverteilten Rewards mit mean [0.5, 0.495]', 'value': 'dist3'}
                                    ],
                                    value='dist1'
                                ),
                                html.Label('Erster Zug'),
                                dcc.Dropdown(
                                    id='first_move',
                                    options=[
                                        {'label': 'Optimaler Arm', 'value': 'optimal'},
                                        {'label': 'Anderer Arm', 'value': 'other'}
                                    ],
                                    value='optimal'
                                ),
                                html.Label('Alpha'),
                                dcc.Dropdown(
                                    id='alpha',
                                    options=[
                                        {'label': '0.01', 'value': '0.01'},
                                        {'label': '0.05', 'value': '0.05'},
                                        {'label': '0.1', 'value': '0.1'}
                                    ],
                                    value='0.01'
                                ),
                                html.Label('Algorithmus für Plot 4'),
                                dcc.Dropdown(
                                    id='Algorithmus',
                                    options=[
                                        {'label': "ETC", 'value': 'ETC'},
                                        {'label': "Greedy", 'value': '0.05'},
                                        {'label': "UCB", 'value': '0.1'}
                                    ],
                                    value='0.01'
                                ),
                            ]
                        ),
                        html.H2("Legende"),
                        html.Ul(
                            children=[html.Li(algo) for algo in [
                                "ETC", "Greedy", "UCB", "UCB-Normal", "UCB-V", "UCB-Tuned", "PAC-UCB", "UCB-Improved", "EUCBV"
                            ]]
                        )
                    ]
                ),
                # Rechte Seite mit Plots
                html.Div(
                    style={'flex': '3', 'padding': '20px'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'flexWrap': 'wrap'},
                            children=[
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[create_dummy_plot("Plot 1")]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[create_dummy_plot("Plot 2")]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[create_dummy_plot("Plot 3")]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[create_dummy_plot("Plot 4")]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[create_dummy_plot("Plot 5")]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[create_dummy_plot("Plot 6")])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Main Funktion um die App zu starten
if __name__ == '__main__':
    app.run_server(debug=True)
