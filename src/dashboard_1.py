import dash
import dash_core_components as dcc
from dash import html
import dash_html_components as html
from dash.dependencies import Input, Output, ALL
import plotly.graph_objs as go
import pandas as pd
import os

# Initialisiere die Dash App
app = dash.Dash(__name__)
app.title = "Simulation of Variance-aware Algorithms for Stochastic Bandit Problems"

# Basis path
base_path = os.path.join(os.getcwd(), "data", "algorithms_results")
var_base_path = os.path.join(os.getcwd(), "data", "algorithms_results", "Value_at_Risk")

# algorithms in structured list
algorithms = {
    "Standard Algorithms": ["1_ETC", "2_Greedy", "3_UCB", "4_UCB-Normal"],
    "Not-variance-aware UCB Variations": ["7_PAC-UCB", "8_UCB-Improved"],
    "Variance-aware UCB Variations": ["5_UCB-Tuned", "6_UCB-V", "9_EUCBV"]
}

# Define the design (color and line style) for groups and algorithms
algorithm_design = {
    "Standard Algorithms": {
        "meta": {"value": "Standard Algorithms", "color": "#58D3F7", "line_style": "solid"},
        "algorithms": [
            {"label": "1_ETC", "value": "1_ETC", "color": "#58D3F7", "line_style": "solid"},
            {"label": "2_Greedy", "value": "2_Greedy", "color": "#58D3F7", "line_style": "solid"},
            {"label": "3_UCB", "value": "3_UCB", "color": "#58D3F7", "line_style": "solid"},
            {"label": "4_UCB-Normal", "value": "4_UCB-Normal", "color": "#58D3F7", "line_style": "solid"},
        ],
    },
    "Not-variance-aware UCB Variations": {
        "meta": {"value": "Not-variance-aware UCB Variations", "color": "#FE2E9A", "line_style": "dot"},
        "algorithms": [
            {"label": "7_PAC-UCB", "value": "7_PAC-UCB", "color": "#FE2E9A", "line_style": "dot"},
            {"label": "8_UCB-Improved", "value": "8_UCB-Improved", "color": "#FE2E9A", "line_style": "dot"},
        ],
    },
    "Variance-aware UCB Variations": {
        "meta": {"value": "Variance-aware UCB Variations", "color": "#D7DF01", "line_style": "dash"},
        "algorithms": [
            {"label": "5_UCB-Tuned", "value": "5_UCB-Tuned", "color": "#D7DF01", "line_style": "dash"},
            {"label": "6_UCB-V", "value": "6_UCB-V", "color": "#D7DF01", "line_style": "dash"},
            {"label": "9_EUCBV", "value": "9_EUCBV", "color": "#D7DF01", "line_style": "dash"},
        ],
    },
}

# Alle Algorithmen extrahieren
all_algorithms = [algo["value"] for group in algorithm_design.values() for algo in group["algorithms"]]

colors = [
    "#58D3F7", "#58D3F7", "#58D3F7", "#58D3F7",
    "#D7DF01", "#D7DF01", "#FE2E9A", "#FE2E9A", "#D7DF01", "#58D3F7", "#FE2E9A", "#D7DF01"
]

line_styles = [
    "solid", "solid", "solid", "solid",
    "dash", "dash", "dot", "dot", "dash", "solid", "dot", "dash"
]

# # Funktion zum Generieren der benutzerdefinierten Checkliste
# def generate_custom_checklist():
#     checklist_items = []
#     algorithm_groups = {
#         "Standard Algorithms": ["1_ETC", "2_Greedy", "3_UCB", "4_UCB-Normal"],
#         "Not-variance-aware UCB Variations": ["7_PAC-UCB", "8_UCB-Improved"],
#         "Variance-aware UCB Variations": ["5_UCB-Tuned", "6_UCB-V", "9_EUCBV"]
#     }

#     for group_name, algorithms in algorithm_groups.items():
#         # Gruppennamen hinzufügen
#         checklist_items.append(
#             html.Div(
#                 group_name, style={"fontWeight": "bold", "marginTop": "10px"}
#             )
#         )
#         # Algorithmen in die Gruppe einfügen
#         for algo in algorithms:
#             checklist_items.append(
#                 dcc.Checklist(
#                     options=[
#                         {
#                             "label": algo,
#                             "value": algo,
#                         }
#                     ],
#                     value=[],  # Standardmäßig nicht ausgewählt
#                     id={"type": "algorithm-checkbox", "index": algo},
#                     style={"marginLeft": "20px"}
#                 )
#             )

#     return html.Div(checklist_items)

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
                font={'color': 'black'}
            )
        }
    )

# Funktion zum Laden der Daten
def load_data(algorithm, arm_distribution, first_move):
    results_path = os.path.join(base_path, f"{algorithm}_results_{first_move}_ver{arm_distribution}.csv")
    average_results_path = os.path.join(base_path, f"{algorithm}_average_results_{first_move}_ver{arm_distribution}.csv")

    df_results = pd.read_csv(results_path)
    df_average = pd.read_csv(average_results_path)

    return df_results, df_average

# Layout der App
app.layout = html.Div(
    style={'backgroundColor': 'white', 'color': 'black', 'font-family': 'Arial, sans-serif'},
    children=[
        html.Div(
            style={'textAlign': 'center', 'padding': '20px'},
            children=[html.H1("Simulation of Variance-aware Algorithms for Stochastic Bandit Problems")]
        ),
        html.Div(
            style={'display': 'flex'},
            children=[
                # Linke Navigationsleiste
                html.Div(
                    style={'flex': '1', 'padding': '20px', 'backgroundColor': '#f0f0f0'},
                    children=[
                        html.H2("Settings"),
                        html.Div(
                            children=[
                                html.Label('Distribution of Arms: [optimal arm, suboptimal arm]'),
                                dcc.Dropdown(
                                    id='arm_distribution',
                                    options=[
                                        {'label': '[0.9, 0.8]', 'value': '1'},
                                        {'label': '[0.9, 0.895]', 'value': '2'},
                                        {'label': '[0.5, 0.495]', 'value': '3'}
                                    ],
                                    placeholder='Select...',
                                    clearable=False,
                                    value='1'
                                ),
                                html.Label('Order of Arms'),
                                dcc.Dropdown(
                                    id='first_move',
                                    options=[
                                        {'label': '(optimal arm, suboptimal arm)', 'value': 'opt'},
                                        {'label': '(suboptimal arm, optimal arm)', 'value': 'subopt'}
                                    ],
                                    placeholder='Select...',
                                    clearable=False,
                                    value='opt'
                                ),
                                html.Label('Alpha for Fig. 5'),
                                dcc.Dropdown(
                                    id='alpha',
                                    options=[
                                        {'label': '0.01', 'value': '0.01'},
                                        {'label': '0.05', 'value': '0.05'},
                                        {'label': '0.1', 'value': '0.1'}
                                    ],
                                    placeholder='Select...',
                                    clearable=False,
                                    value='0.05'
                                ),
                                html.Label('Algorithm for Fig. 4'),
                                dcc.Dropdown(
                                    id='selected_algorithm',
                                    options=[],  # Zunächst leeres Dropdown, wird durch Callback gefüllt
                                    placeholder='Select...',
                                    clearable=False,
                                    value=None  # Initial kein Wert ausgewählt
                                ),
                            ]
                        ),
                        html.Div([
                            html.Label(
                                group["meta"]["value"],
                                style={"color": group["meta"]["color"]}
                            ),
                            dcc.Dropdown(
                                id=f"{group_key}_dropdown",
                                options=[
                                    {"label": algo["label"], "value": algo["value"]}
                                    for algo in group["algorithms"]
                                ],
                                multi=True,
                                placeholder=f"Select {group['meta']['value']} algorithms"
                            )
                        ]) for group_key, group in algorithm_design.items()
                    ]
                ),
                # Rechte Seite mit Plots
                html.Div(
                    style={'flex': '4', 'padding': '20px'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'flexWrap': 'wrap'},
                            children=[
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot1')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot2')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot3')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot4')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot5')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot6')])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
                # Linke Navigationsleiste
                html.Div(
                    style={'flex': '1', 'padding': '20px', 'backgroundColor': '#f0f0f0'},
                    children=[
                        html.H2("Settings"),
                        html.Div(
                            children=[
                                html.Label('Distribution of Arms: [optimal arm, suboptimal arm]'),
                                dcc.Dropdown(
                                    id='arm_distribution',
                                    options=[
                                        {'label': '[0.9, 0.8]', 'value': '1'},
                                        {'label': '[0.9, 0.895]', 'value': '2'},
                                        {'label': '[0.5, 0.495]', 'value': '3'}
                                    ],
                                    placeholder='Select...',
                                    clearable=False,
                                    value='1'
                                ),
                                html.Label('Order of Arms'),
                                dcc.Dropdown(
                                    id='first_move',
                                    options=[
                                        {'label': '(optimal arm, suboptimal arm)', 'value': 'opt'},
                                        {'label': '(suboptimal arm, optimal arm)', 'value': 'subopt'}
                                    ],
                                    placeholder='Select...',
                                    clearable=False,
                                    value='opt'
                                ),
                                html.Label('Alpha for Fig. 5'),
                                dcc.Dropdown(
                                    id='alpha',
                                    options=[
                                        {'label': '0.01', 'value': '0.01'},
                                        {'label': '0.05', 'value': '0.05'},
                                        {'label': '0.1', 'value': '0.1'}
                                    ],
                                    placeholder='Select...',
                                    clearable=False,
                                    value='0.05'
                                ),
                                html.Label('Algorithm for Fig. 4'),
                                dcc.Dropdown(
                                    id='selected_algorithm',
                                    options=[],  # Zunächst leeres Dropdown, wird durch Callback gefüllt
                                    placeholder='Select...',
                                    clearable=False,
                                    value=None  # Initial kein Wert ausgewählt
                                ),
                            ]
                        ),
                        html.Div([
                            html.Label(
                                group["meta"]["value"],
                                style={"color": group["meta"]["color"]}
                            ),
                            dcc.Dropdown(
                                id=f"{group_key}_dropdown",
                                options=[
                                    {"label": algo["label"], "value": algo["value"]}
                                    for algo in group["algorithms"]
                                ],
                                multi=True,
                                placeholder=f"Select {group['meta']['value']} algorithms"
                            )
                        ]) for group_key, group in algorithm_design.items()
                    ]
                )
                # Rechte Seite mit Plots
                html.Div(
                    style={'flex': '4', 'padding': '20px'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'flexWrap': 'wrap'},
                            children=[
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot1')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot2')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot3')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot4')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot5')]),
                                html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot6')])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# # Layout der App
# app.layout = html.Div(
#     style={'backgroundColor': 'white', 'color': 'black', 'font-family': 'Arial, sans-serif'},
#     children=[
#         html.Div(
#             style={'textAlign': 'center', 'padding': '20px'},
#             children=[
#                 html.H1("Simulation of Variance-aware Algorithms for Stochastic Bandit Problems")
#             ]
#         ),
#         html.Div(
#             style={'display': 'flex'},
#             children=[
#                 # Linke Navigationsleiste
#                 html.Div(
#                     style={'flex': '1', 'padding': '20px', 'backgroundColor': '#f0f0f0'},
#                     children=[
#                         html.H2("Settings"),
#                         html.Div(
#                             children=[
#                                 html.Label('Distribution of Arms: [optimal arm, suboptimal arm]'),
#                                 dcc.Dropdown(
#                                     id='arm_distribution',
#                                     options=[
#                                         {'label': '[0.9, 0.8]', 'value': '1'},
#                                         {'label': '[0.9, 0.895]', 'value': '2'},
#                                         {'label': '[0.5, 0.495]', 'value': '3'}
#                                     ],
#                                     placeholder='Select...',  # Dies entfernt die "Select..."-Option
#                                     clearable=False,
#                                     value='1'
#                                 ),
#                                 html.Label('Order of Arms'),
#                                 dcc.Dropdown(
#                                     id='first_move',
#                                     options=[
#                                         {'label': '(optimal arm, suboptimal arm)', 'value': 'opt'},
#                                         {'label': '(suboptimal arm, optimal arm)', 'value': 'subopt'}
#                                     ],
#                                     placeholder='Select...',  
#                                     clearable=False,
#                                     value='opt'
#                                 ),
#                                 html.Label('Alpha for Fig. 5'),
#                                 dcc.Dropdown(
#                                     id='alpha',
#                                     options=[
#                                         {'label': '0.01', 'value': '0.01'},
#                                         {'label': '0.05', 'value': '0.05'},
#                                         {'label': '0.1', 'value': '0.1'}
#                                     ],
#                                     placeholder='Select...',  
#                                     clearable=False,
#                                     value='0.05'
#                                 ),
#                                 # html.Label('Algorithm for Fig. 4'),
#                                 # dcc.Dropdown(
#                                 #     id='selected_algorithm',
#                                 #     options=[{'label': algo, 'value': algo} for algo in algorithm_data],
#                                 #     placeholder='Select...',  
#                                 #     clearable=False, 
#                                 #     value='3_UCB'
#                                 # ),
#                                 html.Label('Algorithm for Fig. 4'),
#                                 dcc.Dropdown(
#                                     id='selected_algorithm',
#                                     options=[],  # Zunächst leeres Dropdown, wird durch Callback gefüllt
#                                     placeholder='Select...',
#                                     clearable=False,
#                                     value=None  # Initial kein Wert ausgewählt
#                                  ),
#                                 html.Label('Selected Algorithms'),
#                                 dcc.Checklist(
#                                     options=algorithms,
#                                     value=[],
#                                     id=f"{group}-checklist",
#                                     inline=True
#                                 )
#                             ]) for group, algorithms in algorithm_design.items()
#             ])
#                             ],
#                         ),

#                     ],
#                 ),
#                 # Rechte Seite mit Plots
#                 html.Div(
#                     style={'flex': '4', 'padding': '20px'},
#                     children=[
#                         html.Div(
#                             style={'display': 'flex', 'flexWrap': 'wrap'},
#                             children=[
#                                 html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot1')]),
#                                 html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot2')]),
#                                 html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot3')]),
#                                 html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot4')]),
#                                 html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot5')]),
#                                 html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot6')])
#                             ]
#                         )
#                     ]
#                 )
#             ]
#         )
#     ]
# )
# Callback zum Aktualisieren des Dropdowns basierend auf den ausgewählten Algorithmen
@app.callback(
    Output('selected_algorithm', 'options'),
    [Input({"type": "algorithm-checkbox", "index": ALL}, "value")]
)
def update_output(selected_values):
    # Ermitteln, welche Algorithmen ausgewählt wurden
    selected_algorithms = []
    for group in algorithm_design.values():
        for algo in group['algorithms']:
            if algo['value'] in selected_values:
                selected_algorithms.append(algo['value'])
    
    return [{'label': algo, 'value': algo} for algo in selected_algorithms]

def update_dropdown(selected_algorithms):
    # Dropdown-Optionen auf die ausgewählten Algorithmen aus der Checkliste beschränken
    if not selected_algorithms:
        return []
    
    # Erstelle Optionen für das Dropdown-Menü
    return [{'label': algo, 'value': algo} for algo in selected_algorithms]

def update_selection(selected_values):
    # Kopiere die aktuelle Auswahl
    updated_selection = set(selected_values)

    # Zeige die ausgewählten Algorithmen an
    output = []
    
    # Iteriere über die ausgewählten Algorithmen
    for algo in selected_values:
        # Überprüfe, ob das Element kein Gruppenname ist
        if algo not in algorithms.keys():  
            try:
                # Verwende nur den Algorithmusnamen zum Laden der Ergebnisse
                df_results, df_average = load_data(algo)
                output.append(html.Div(f"Ergebnisse für {algo}: {df_results.head()}"))  # Zeige die ersten Zeilen des DataFrames an
            except FileNotFoundError as e:
                output.append(html.Div(str(e)))

    return output


# Callback zum Aktualisieren der Plots
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure'),
     Output('plot5', 'figure'),
     Output('plot6', 'figure')],
    [Input({"type": "algorithm-checkbox", "index": ALL}, "value"),
     Input('selected_algorithm', 'value'),
     Input('arm_distribution', 'value'),
     Input('first_move', 'value'),
     Input('alpha', 'value')]
)

def update_plots(selected_algorithms, selected_algorithm, arm_distribution, first_move, selected_alpha):
    #initialise empty figures
    fig1, fig2, fig3, fig4, fig5, fig6 = [go.Figure() for _ in range(6)]

    # laod data
    data = {}
    for algo in selected_algorithms:
        data[algo] = load_data(algo, arm_distribution, first_move)
         # Determine the color and line style
        if algo in algorithms:
            # Use the group color and line style
            color = colors[list(algorithms.keys()).index(algo)]
            line_style = line_styles[list(algorithms.keys()).index(algo)]
        else:
            # Use the algorithm color and line style
            color_idx = all_algorithms.index(algo)
            color = colors[color_idx]
            line_style = line_styles[color_idx]

    # Plot 1: Average Total Reward
    fig1 = go.Figure()
    for algo, color, line_style in zip(selected_algorithms, colors, line_styles):
        df = data[algo][1]
        fig1.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Total Reward'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color, dash=line_style)
        ))
    fig1.update_layout(
        title='Fig. 1: Average Total Reward over Time',
        xaxis_title="Timesteps",
        yaxis_title="Average Total Reward",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=False
    )

    # Plot 2: Average Regret
    fig2 = go.Figure()
    for algo, color, line_style in zip(selected_algorithms, colors, line_styles):
        df = data[algo][1]
        fig2.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Regret'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color, dash=line_style)
        ))
    fig2.update_layout(
        title='Fig.2: Average Total Regret over Time',
        xaxis_title="Timesteps",
        yaxis_title="Average Total Regret",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=False
    )

    # Plot 3: Average Zeros and Ones Count
    fig3 = go.Figure()

    # Datenstrukturen zum Speichern der Werte
    zeros_counts = []
    ones_counts = []
    algo_labels_zeros = []
    algo_labels_ones = []

    # Durchlaufe die Algorithmen
    for algo in selected_algorithms:
        # Laden der Daten für den spezifischen Algorithmus
        df_results, df_average = data[algo]
        
        # Extrahieren der Werte
        zero_count = df_average['Average Zeros Count'].iloc[-1]
        one_count = df_average['Average Ones Count'].iloc[-1]
        
        # Hinzufügen der Werte zur Liste
        zeros_counts.append(zero_count)
        ones_counts.append(one_count)
        
        # Erstellen der Labels für die X-Achse
        algo_labels_zeros.append(f'{algo} - Zeros')
        algo_labels_ones.append(f'{algo} - Ones')

    # Erstellen der Balken für die Average Zeros Count
    fig3.add_trace(go.Bar(
        x=algo_labels_zeros,
        y=zeros_counts,
        name='Average Zeros Count',
        marker_color='blue'
    ))

    # Erstellen der Balken für die Average Ones Count
    fig3.add_trace(go.Bar(
        x=algo_labels_ones,
        y=ones_counts,
        name='Average Ones Count',
        marker_color='orange'
    ))

    # Layout-Anpassungen
    fig3.update_layout(
        title='Fig. 3: Average Zeros and Ones Count',
        xaxis_title='Algorithm',
        yaxis_title='Count',
        barmode='group',
        xaxis=dict(
            tickvals=list(range(len(algo_labels_zeros) + len(algo_labels_ones))),
            ticktext=algo_labels_zeros + algo_labels_ones,
            tickangle=45
        )
    )

    # # Plot 4: Distribution of Total Regret at Timestep 100000
    # selected_data = data[selected_algorithm][0]
    # df_100k = selected_data[selected_data['Timestep'] == 100000]
    # fig4 = go.Figure(go.Histogram(x=df_100k['Total Regret'], marker_color=colors[algorithm_data.index(selected_algorithm)]))
    # fig4.update_layout(
    #     title=f'Fig. 4: Distribution of Total Regret at Time 100 000 for {selected_algorithms}',
    #     xaxis_title="Total Regret",
    #     yaxis_title="Count",
    #     paper_bgcolor='white',
    #     plot_bgcolor='white',
    #     font={'color': 'black'},
    #     showlegend=False
    # )

    # if selected_algorithm:
    #     selected_data = data[selected_algorithm][0]
    #     df_100k = selected_data[selected_data['Timestep'] == 100000]
    #     fig4 = go.Figure(go.Histogram(x=df_100k['Total Regret'], marker_color=colors[algorithm_data.index(selected_algorithm)]))
    #     fig4.update_layout(
    #         title=f'Fig. 4: Distribution of Total Regret at Time 100 000 for {selected_algorithm}',
    #         xaxis_title="Total Regret",
    #         yaxis_title="Count",
    #         paper_bgcolor='white',
    #         plot_bgcolor='white',
    #         font={'color': 'black'},
    #         showlegend=False
    #     )
    # else:
    #     # Fallback, wenn kein Algorithmus ausgewählt ist
    #     fig4 = go.Figure()

    


    # Plot 5: Value at Risk Function
    alpha_value = float(selected_alpha)
    
    fig5 = go.Figure()
    for algo, color, line_style in zip(selected_algorithms, colors, line_styles):
        var_file = os.path.join(var_base_path, f"{algo}_VaR_alpha_{alpha_value}.csv")
        df_var = pd.read_csv(var_file)
        
        fig5.add_trace(go.Scatter(
            x=df_var['Timestep'],
            y=df_var['Value_at_Risk'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color, dash=line_style)
        ))
    
    fig5.update_layout(
        title=f'Fig. 5: Value at Risk for selected alpha={selected_alpha}',
        xaxis_title="Timesteps",
        yaxis_title="Value at Risk",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=True
    )

    # Plot 6: Fraction of Suboptimal Arms Pulled
    fig6 = go.Figure()
    for algo, color, line_style in zip(selected_algorithms, colors, line_styles):
        df = data[algo][1]
        fig6.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Suboptimal Arms'] / df['Timestep'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color, dash=line_style)
        ))
    fig6.update_layout(
        title='Fig. 6: Proportion of Suboptimal Arms pulled in comparison to all Arms pulled',
        xaxis_title="Timesteps",
        yaxis_title="Proportion of Suboptimal Arms",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=False
    )

    return fig1, fig2, fig3, fig1, fig5, fig6

# Start Dash App
if __name__ == '__main__':

    app.run_server(debug=True)
