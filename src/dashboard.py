import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os

# Initialise Dash App
app = dash.Dash(__name__)
app.title = "Simulation of variance-aware algorithms for Stochastic Bandit Problems"

# Basis path
base_path = os.path.join(os.getcwd(), "data", "algorithms_results")
var_base_path = os.path.join(os.getcwd(), "data", "algorithms_results", "Value_at_Risk")

# Algorithms, add new algorithms here
algorithm_data = [
    {"label": "Standard Algorithms", "value": "Standard Algorithms", "color": "#00FF00", "line_style": "solid"},
    {"label": "ETC", "value": "ETC", "color": "#32CD32", "line_style": "solid"},
    {"label": "Greedy", "value": "Greedy", "color": "#9ACD32", "line_style": "solid"},
    {"label": "UCB", "value": "UCB", "color": "#6B8E23", "line_style": "solid"},
    #{"label": "UCB-Normal", "value": "UCB-Normal", "color": "#808000", "line_style": "solid"},
    
    {"label": "Not-variance-aware UCB Variations", "value": "Not-variance-aware UCB Variations", "color": "#00CED1", "line_style": "dot"},
    {"label": "PAC-UCB", "value": "PAC-UCB", "color": "#00BFFF", "line_style": "dot"},
    {"label": "UCB-Improved", "value": "UCB-Improved", "color": "#4169E1", "line_style": "dot"},

    {"label": "Variance-aware UCB Variations", "value": "Variance-aware UCB Variations", "color": "#BC8F8F", "line_style": "dash"},
    {"label": "UCB-Tuned", "value": "UCB-Tuned", "color": "#DAA520", "line_style": "dash"},
    {"label": "UCB-V", "value": "UCB-V", "color": "#D2691E", "line_style": "dash"},
    {"label": "EUCBV", "value": "EUCBV", "color": "#800000", "line_style": "dash"}
]

def load_data(algorithm, arm_distribution):
    #def load_data(algorithm, arm_distribution, first_move):
    """
    Loads results and average results data for a specified algorithm and arm distribution.
    Parameters:
    algorithm (str): The name of the algorithm for which to load data.
    arm_distribution (str): The version of the arm distribution.
    first_move (str): The first move identifier.
    Returns:
    tuple: A tuple containing two pandas DataFrames:
        - df_results: DataFrame containing the results data.
        - df_average: DataFrame containing the average results data.
    """

    results_path = os.path.join(base_path, f"{algorithm}_results_{arm_distribution}.csv")
    average_results_path = os.path.join(base_path, f"{algorithm}_average_results_{arm_distribution}.csv")

    df_results = pd.read_csv(results_path)
    df_average = pd.read_csv(average_results_path)

    return df_results, df_average

# Layout of the Dash App
# Define the layout of the Dash App
app.layout = html.Div(
    style={'backgroundColor': 'white', 'color': 'black', 'font-family': 'Arial, sans-serif'},
    children=[
        # Header section
        html.Div(
            style={'textAlign': 'center', 'padding': '20px'},
            children=[
                html.H1("Simulation of Variance-aware Algorithms for Stochastic Bandit Problems")
            ]
        ),
        # Main content section
        html.Div(
            style={'display': 'flex'},
            children=[
                # Settings panel
                html.Div(
                    style={'flex': '1', 'padding': '20px', 'backgroundColor': '#f0f0f0'},
                    children=[
                        html.H2("Settings"),
                        html.Div(
                            style={'flex': '1', 'backgroundColor': '#f0f0f0'},
                            children=[
                                # Checklist for selecting algorithms
                                *[
                                    html.Div(
                                    style={'margin-bottom': '20px'},
                                    children=[
                                        html.Div([
                                            dcc.Checklist(
                                                id=f"{algo['value']}_checklist",
                                                options=[
                                                    {"label": algo["label"], "value": algo["value"]}
                                                ],
                                                value=[algo["value"]],
                                                labelStyle={
                                                    "color": algo["color"],
                                                    'display': 'block',
                                                    "margin-left": "20px" if "ETC" in algo["value"] or 
                                                                    "Greedy" in algo["value"] or 
                                                                    "UCB" in algo["value"] or 
                                                                    #"UCB-Normal" in algo["value"] or 
                                                                    "PAC-UCB" in algo["value"] or 
                                                                    "UCB-Improved" in algo["value"] or
                                                                    "UCB-Tuned" in algo["value"] or 
                                                                    "UCB-V" in algo["value"] or 
                                                                    "EUCBV" in algo["value"] else "0px"
                                                }
                                            )
                                        ]) for algo in algorithm_data
                                    ]
                                    )
                                ],
                                # Dropdown for selecting arm distribution
                                html.Label('Distribution of Arms', style={'margin-top': '10px'}),
                                dcc.Dropdown(
                                    id='arm_distribution',
                                    options=[
                                        {'label': '[0.9, 0.8, 0.7]', 'value': '900_800_700'},
                                        {'label': '[0.9, 0.85, 0.8]', 'value': '900_850_800'},
                                        {'label': '[0.9, 0.8]', 'value': '900_800'},
                                    ],
                                    placeholder='Select...',  
                                    clearable=False,
                                    value='900_800_700',
                                    style={'margin-bottom': '10px'}
                                ),
                                # Dropdown for selecting order of arms
                                # html.Label('Order of Arms', style={'margin-top': '10px'}),
                                # dcc.Dropdown(
                                #     id='first_move',
                                #     options=[
                                #         {'label': '(optimal arm, suboptimal arm)', 'value': 'opt'},
                                #         {'label': '(suboptimal arm, optimal arm)', 'value': 'subopt'}
                                #     ],
                                #     placeholder='Select...',  
                                #     clearable=False,
                                #     value='opt',
                                #     style={'margin-bottom': '10px'}
                                #),
                                # Dropdown for selecting alpha value
                                html.Label('Alpha for Fig. 5', style={'margin-top': '10px'}),
                                dcc.Dropdown(
                                    id='alpha',
                                    options=[
                                        {'label': '0.01', 'value': '0.01'},
                                        {'label': '0.05', 'value': '0.05'},
                                        {'label': '0.1', 'value': '0.1'}
                                    ],
                                    placeholder='Select...',  
                                    clearable=False,
                                    value='0.05',
                                    style={'margin-bottom': '10px'}
                                ),
                                # Dropdown for selecting algorithm for Fig. 4
                                html.Label('Algorithm for Fig. 4', style={'margin-top': '10px'}),
                                dcc.Dropdown(
                                    id='selected_algorithm',
                                    options=[{'label': algo['label'], 'value': algo['value']} for algo in algorithm_data],  
                                    placeholder='Select...',
                                    clearable=False,
                                    value='3_UCB',
                                    style={'margin-bottom': '10px'}
                                ),
                            ]
                        ),
                    ]
                ),
                # Plots panel
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

# Callback for updating the plots
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure'),
     Output('plot5', 'figure'),
     Output('plot6', 'figure')],
    [Input(f"{algo['value']}_checklist", 'value') for algo in algorithm_data] +
    [Input('selected_algorithm', 'value'),
     Input('arm_distribution', 'value'),
     #Input('first_move', 'value'),
     Input('alpha', 'value')]
)

def update_plots(*args):
    """
    Update and generate various plots based on the provided algorithm data and parameters.
    Parameters:
    *args: Variable length argument list containing:
        - selected_algorithms (list): List of selected algorithms.
        - selected_algorithm (str): The algorithm selected for specific plots.
        - arm_distribution (str): The distribution of arms.
        #- first_move (str): The first move parameter.
        - selected_alpha (float): The alpha value for the Value at Risk plot.
    Returns:
    tuple: A tuple containing six plotly.graph_objects.Figure objects:
        - fig1: Average Total Reward over Time.
        - fig2: Average Total Regret over Time.
        - fig3: Average Zeros and Ones Count.
        - fig4: Distribution of Total Regret at Timestep 100000.
        - fig5: Value at Risk for the selected alpha.
        - fig6: Proportion of Suboptimal Arms pulled / all Arms pulled.
    """

    # Extract the selected algorithms and parameters from the arguments
    selected_algorithms = [algo for algo_values in args[:len(algorithm_data)] for algo in algo_values]
    selected_algorithm = args[len(algorithm_data)]
    arm_distribution = args[len(algorithm_data) + 1]
    #first_move = args[len(algorithm_data) + 2]
    selected_alpha = args[len(algorithm_data) + 2]

    # Initialize empty figures
    fig1, fig2, fig3, fig4, fig5, fig6 = [go.Figure() for _ in range(6)]

    # Load data for each selected algorithm
    data = {}
    for algo in selected_algorithms:
        #data[algo] = load_data(algo, arm_distribution, first_move)
        data[algo] = load_data(algo, arm_distribution)

    # Plot 1: Average Total Reward
    fig1 = go.Figure()
    for algo in selected_algorithms:
        df = data[algo][1]
        algo_data = next((a for a in algorithm_data if a["value"] == algo), None)
        if algo_data:
            fig1.add_trace(go.Scatter(
                x=df['Timestep'],
                y=df['Average Total Reward'],
                mode='lines+markers',
                name=algo,
                line=dict(color=algo_data["color"], dash=algo_data["line_style"])
            ))
    fig1.update_layout(
        title='Fig. 1: Average Total Reward over Time',
        xaxis_title="Timesteps",
        yaxis_title="Average Total Reward",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black', "size": 8},
        showlegend=False
    )

    # Plot 2: Average Regret
    fig2 = go.Figure()
    for algo in selected_algorithms:
        df = data[algo][1]
        algo_data = next((a for a in algorithm_data if a["value"] == algo), None)
        if algo_data:
            fig2.add_trace(go.Scatter(
                x=df['Timestep'],
                y=df['Average Regret'],
                mode='lines+markers',
                name=algo,
                line=dict(color=algo_data["color"], dash=algo_data["line_style"])
            ))
    fig2.update_layout(
        title='Fig.2: Average Total Regret over Time',
        xaxis_title="Timesteps",
        yaxis_title="Average Total Regret",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black', "size": 8},
        showlegend=False
    )

    # Plot 3: Average Zeros and Ones Count
    fig3 = go.Figure()

    zeros_counts = []
    ones_counts = []
    algo_labels = []
    colors_zeros = []
    colors_ones = []

    for algo in selected_algorithms:
        # Load data for the specific algorithm
        df_results, df_average = data[algo]
        
        # Extract values
        zero_count = df_average['Average Zeros Count'].iloc[-1]
        one_count = df_average['Average Ones Count'].iloc[-1]
        
        # Add values to the list
        zeros_counts.append(zero_count)
        ones_counts.append(one_count)
        
        # Create labels for the x-axis
        algo_labels.append(algo)

        # Extract the color of the algorithm
        algo_data = next((a for a in algorithm_data if a["value"] == algo), None)
        if algo_data:
            colors_zeros.append(algo_data["color"])
            colors_ones.append(algo_data["color"])

    # Create bars for the Average Zeros Count
    fig3.add_trace(go.Bar(
        x=algo_labels,
        y=zeros_counts,
        name='Average Zeros Count',
        marker_color=colors_zeros,
        text=None  # Remove descriptions
    ))

    # Create bars for the Average Ones Count
    fig3.add_trace(go.Bar(
        x=algo_labels,
        y=ones_counts,
        name='Average Ones Count',
        marker_color=colors_ones,
        text=None  # Remove descriptions
    ))

    # Layout adjustments
    fig3.update_layout(
        title='Fig. 3: Average Zeros and Ones Count',
        xaxis_title='Algorithm',
        yaxis_title='Count',
        barmode='group',
        xaxis=dict(
            tickvals=list(range(len(algo_labels))),
            ticktext=algo_labels,
            tickangle=45
        ),
        font={'color': 'black', "size": 8},
        showlegend=False  # Hide legend
    )

    # Plot 4: Distribution of Total Regret at Timestep 100000
    selected_data = data[selected_algorithm][0]
    df_100k = selected_data[selected_data['Timestep'] == 100000]
    # Find the color for the selected algorithm
    selected_algo_info = next((algo for algo in algorithm_data if algo['value'] == selected_algorithm), None)
    if selected_algo_info:
        selected_color = selected_algo_info['color']
    else:
        selected_color = 'black'
    
    fig4 = go.Figure(go.Histogram(x=df_100k['Total Regret'], marker_color=selected_color))
    fig4.update_layout(
        title=f'Fig. 4: Distribution of Total Regret at t=100 000 for {selected_algorithm}',
        xaxis_title="Total Regret",
        yaxis_title="Count",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black', "size": 8},
        showlegend=False
    )

    # Plot 5: Value at Risk Function
    alpha_value = float(selected_alpha)
    
    fig5 = go.Figure()
    for algo in selected_algorithms:
        var_file = os.path.join(var_base_path, f"{algo}_VaR_{arm_distribution}_alpha_{alpha_value}.csv")
        df_var = pd.read_csv(var_file)
        algo_data = next((a for a in algorithm_data if a["value"] == algo), None)
        if algo_data:
            fig5.add_trace(go.Scatter(
                x=df_var['Timestep'],
                y=df_var['Value_at_Risk'],
                mode='lines+markers',
                name=algo,
                line=dict(color=algo_data["color"], dash=algo_data["line_style"])
            ))
    
    fig5.update_layout(
        title=f'Fig. 5: Value at Risk for selected alpha={selected_alpha}',
        xaxis_title="Timesteps",
        yaxis_title="Value at Risk",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black', "size": 8},
        showlegend=False
    )

    # Plot 6: Fraction of Suboptimal Arms Pulled
    fig6 = go.Figure()
    for algo in selected_algorithms:
        df = data[algo][1]
        algo_data = next((a for a in algorithm_data if a["value"] == algo), None)
        if algo_data:
            fig6.add_trace(go.Scatter(
                x=df['Timestep'],
                y=df['Average Suboptimal Arms'] / df['Timestep'],
                mode='lines+markers',
                name=algo,
                line=dict(color=algo_data["color"], dash=algo_data["line_style"])
            ))
    fig6.update_layout(
        title='Fig. 6: Proportion Suboptimal Arms pulled / all Arms pulled',
        xaxis_title="Timesteps",
        yaxis_title="Proportion of Suboptimal Arms",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black', "size": 8},
        showlegend=False
    )

    return fig1, fig2, fig3, fig4, fig5, fig6

# Start Dash App
if __name__ == '__main__':

    app.run_server(debug=True)
