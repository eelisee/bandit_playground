import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os

# Initialisiere die Dash App
app = dash.Dash(__name__)
app.title = "Simulation of variance-aware algorithms for Stochastic Bandit Problems"

# Dateipfade der CSV-Dateien
base_path = r"C:/Users/canis/OneDrive/Dokumente/uni/uni-surface/FSS 2024/BA/bachelorarbeit_vrlfg/BA/github/BA_code/2_algorithms_results"
algorithm_data= [
    "1_ETC", "2_Greedy", "3_UCB", "4_UCB-Normal", "5_UCB-Tuned", "6_UCB-V", "7_PAC_UCB", "8_UCB_Improved", "9_EUCBV"
]

algorithms = [
    "ETC", "Greedy", "UCB", "UCB-Normal", "UCB-Tuned", "UCB-V", "PAC-UCB", "UCB-Improved", "EUCBV"
]
colors = [
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple'
]

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
            children=[
                html.H1("Simulation of Variance-aware Algorithms for Stochastic Bandit Problems")
            ]
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
                                html.Label('Distribution of Arms'),
                                dcc.Dropdown(
                                    id='arm_distribution',
                                    options=[
                                        {'label': '&mu* = 0.9, &mu_suboptimal = 0.8', 'value': '1'},
                                        {'label': '&mu* = 0.9, &mu_suboptimal = 0.895', 'value': '2'},
                                        {'label': '&mu* = 0.5, &mu_suboptimal = 0.495', 'value': '3'}
                                    ],
                                    placeholder='Select...',  # Dies entfernt die "Select..."-Option
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
                                html.Label('Alpha'),
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
                                html.Label('Algorithm for Fig. 5'),
                                dcc.Dropdown(
                                    id='selected_algorithm',
                                    options=[{'label': algo, 'value': algo} for algo in algorithm_data],
                                    placeholder='Select...',  
                                    clearable=False, 
                                    value='3_UCB'
                                ),
                            ]
                        ),
                        html.H2("Legend"),
                        html.Ul(
                            children=[html.Li(algo, style={'color': color}) for algo, color in zip(algorithms, colors)]
                        )
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

# Callback zum Aktualisieren der Plots
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure'),
     #Output('plot5', 'figure'),
     Output('plot6', 'figure')],
    [Input('selected_algorithm', 'value'),
     Input('arm_distribution', 'value'),
     Input('first_move', 'value'),
     Input('alpha', 'value')]
)
def update_plots(selected_algorithm, arm_distribution, first_move, selected_alpha):
    # lod data
    data = {}
    for algo in algorithm_data:
        data[algo] = load_data(algo, arm_distribution, first_move)

    # Plot 1: Average Total Reward
    fig1 = go.Figure()
    for algo, color in zip(algorithm_data, colors):
        df = data[algo][1]
        fig1.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Total Reward'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color)
        ))
    fig1.update_layout(
        title='Fig. 1: Average Total Reward over Timesteps',
        xaxis_title="Timesteps",
        yaxis_title="Average Total Reward",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=False
    )

    # Plot 2: Average Regret
    fig2 = go.Figure()
    for algo, color in zip(algorithm_data, colors):
        df = data[algo][1]
        fig2.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Regret'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color)
        ))
    fig2.update_layout(
        title='Fig.2: Average Total Regret over Timesteps',
        xaxis_title="Timesteps",
        yaxis_title="Average Total Regret",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=False
    )

    # Plot 3: Boxplot
    fig3 = go.Figure()
    for algo, color in zip(algorithm_data, colors):
        df = data[algo][1]
        fig3.add_trace(go.Box(
            y=[df['Average Zeros Count'].iloc[-1]],
            name=f'{algo} - Zeros',
            marker_color=color
        ))
        fig3.add_trace(go.Box(
            y=[df['Average Ones Count'].iloc[-1]],
            name=f'{algo} - Ones',
            marker_color=color
        ))
    fig3.update_layout(
        title='Fig.3: Count of Zeros and Ones',
        xaxis_title="Zeros and Ones",
        yaxis_title="Count",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=False
    )

     # Plot 4: Distribution of Total Regret at Timestep 100000
    selected_data = data[selected_algorithm][0]
    df_100k = selected_data[selected_data['Timestep'] == 100000]
    fig4 = go.Figure(go.Histogram(x=df_100k['Total Regret'], marker_color=colors[algorithm_data.index(selected_algorithm)]))
    fig4.update_layout(
        title=f'Distribution of Total Regret at Timestep 100.000 for {selected_algorithm}',
        xaxis_title="Total Regret",
        yaxis_title="Count",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=False
    )

    # Plot 4: Distribution of Total Regret at Timestep 100000
    # selected_data = data[selected_algorithm][0]
    # df_100k = selected_data[selected_data['Timestep'] == 100000]
    # fig4 = go.Figure(go.Histogram(x=df_100k['Total Regret'], marker_color=colors[algorithm_data.index(selected_algorithm)]))
    # fig4.update_layout(
    #     title=f'Distribution of Total Regret at Timestep 100.000 for {selected_algorithm}',
    #     xaxis_title="Total Regret",
    #     yaxis_title="Count",
    #     paper_bgcolor='white',
    #     plot_bgcolor='white',
    #     font={'color': 'black'},
    #     showlegend=False
    # )

    # Plot 5: Value at Risk Function
    # fig5 = go.Figure()
    # for algo, color in zip(algorithm_data, colors):
    #     df = data[algo][0]
    #     timesteps = df['Timestep'].unique()
    #     VaR_values = [df[df['Timestep'] == t]['Total Regret'].quantile(1 - selected_alpha) for t in timesteps]
    #     fig5.add_trace(go.Scatter(
    #         x=timesteps,
    #         y=VaR_values,
    #         mode='lines+markers',
    #         name=algo,
    #         line=dict(color=color)
    #     ))

    # Plot 5: Value at Risk Function
    # fig5 = go.Figure()
    # for algo, color in zip(algorithm_data, colors):
    #     df = data[algo][1]
    #     VaR_values = df.groupby('Timestep')['Average Regret'].apply(lambda x: x.quantile(selected_alpha))
    #     fig5.add_trace(go.Scatter(
    #         x=df['Timestep'].unique(),
    #         y=VaR_values,
    #         mode='lines+markers',
    #         name=algo,
    #         line=dict(color=color)
    #     ))

    # # Plot 5: Empirical Means over Timesteps
    # fig5 = go.Figure()
    # for algo, color in zip(algorithm_data, colors):
    #     df = data[algo][1]
    #     fig5.add_trace(go.Scatter(
    #         x=df['Timestep'],
    #         y=df['Empirical Means'],
    #         mode='lines+markers',
    #         name=algo,
    #         line=dict(color=color)
    #     ))
    # fig5.update_layout(
    #     title=f'Value at Risk for selected alpha={selected_alpha}',
    #     xaxis_title="Timesteps",
    #     yaxis_title="Value at Risk",
    #     paper_bgcolor='white',
    #     plot_bgcolor='white',
    #     font={'color': 'black'},
    #     showlegend=False
    # )

    # Plot 6: Fraction of Suboptimal Arms Pulled
    fig6 = go.Figure()
    for algo, color in zip(algorithm_data, colors):
        df = data[algo][1]
        fig6.add_trace(go.Scatter(
            x=df['Timestep'],
            y=df['Average Suboptimal Arms'] / df['Timestep'],
            mode='lines+markers',
            name=algo,
            line=dict(color=color)
        ))
    fig6.update_layout(
        title='Proportion of Suboptimal Arms pulled in comparison to all Arms pulled',
        xaxis_title="Timesteps",
        yaxis_title="Proportion of Suboptimal Arms",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black'},
        showlegend=False
    )

    
    return fig1, fig2, fig3, fig4, fig6

    #return fig1, fig2, fig3, fig4, fig5, fig6

# Start Dash App
if __name__ == '__main__':
    app.run_server(debug=True)
