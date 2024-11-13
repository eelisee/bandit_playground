import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os

from main_script import individual_arm_distribution, algorithm_strategy_pairs, get_directory_for_algorithm, create_directory, algorithm_groups

# Initialise Dash App
app = dash.Dash(__name__, suppress_callback_exceptions=True)
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

# Create a mapping of algorithm names with their corresponding IDs
algorithm_id_mapping = {f"{algo.name}_{index}": (algo, config) for index, (algo, config) in enumerate(algorithm_strategy_pairs)}

# Helper function to find color and line style
def find_algorithm_style(algo_name):
    for algo in algorithm_data:
        if algo["value"] == algo_name:
            return algo["color"], algo["line_style"]
    return "#000000", "solid"  # Default color and line style

# 1. Parse the algorithms from main_script.py
def get_algorithm_data():
    algo_data = []
    for index, (algo, config) in enumerate(algorithm_strategy_pairs):
        algo_name = algo.name
        params = config["params"]
        label = algo_name
        color, line_style = find_algorithm_style(algo_name)  # Use helper function
        
        algo_data.append({
            "label": label,  # This is updated dynamically with parameters later
            "value": algo_name,
            "color": color,
            "line_style": line_style,
            "params": params,  # Store params for later use
            "index": index,  # Add index to ensure unique IDs
            "id": f"{algo_name}_{index}"  # Add ID for unique identification
        })
    return algo_data

algorithm_data = get_algorithm_data()

def get_label_with_params(algo_name, params):
    param_str = ", ".join([f"{k}={v}" for k, v in params.items()])
    return f"{algo_name} ({param_str})"

def load_data(algorithm_with_index, arm_1, arm_2, arm_3):
    """
    Loads results and average results data for a specified algorithm and arm distribution.
    
    Parameters:
    algorithm_with_index (str): The name of the algorithm with index (e.g., "UCB_0").
    arm_1 (str): The selected value for the first arm distribution.
    arm_2 (str): The selected value for the second arm distribution.
    arm_3 (str): The selected value for the third arm distribution (can be "-").
    
    Returns:
    tuple: A tuple containing two pandas DataFrames:
        - df_results: DataFrame containing the results data.
        - df_average: DataFrame containing the average results data.
    """

    algorithm_id = algorithm_with_index
    
    # Extract the actual algorithm name from the combined string
    algorithm = algorithm_with_index.split('_')[0]
    
    # Combine arm distributions into a string for the file name
    if arm_3 == '-' or arm_3 is None:
        arm_distribution = f"{arm_1}_{arm_2}"
    else:
        arm_distribution = f"{arm_1}_{arm_2}_{arm_3}"

    # Find the corresponding algorithm configuration
    algo, algo_config = algorithm_id_mapping.get(algorithm_id, (None, None))
    #algo_config = next((config for algo, config in algorithm_strategy_pairs if algo.name == algorithm), None)
    if not algo_config:
        raise ValueError(f"No configuration found for algorithm: {algorithm}")

    # Generate the parameter directory string
    params = algo_config["params"]
    if params:
        param_dir = '_'.join([f'{key}_{str(value).replace(".", "_")}' for key, value in params.items()])
    else:
        param_dir = 'default'

    # Construct the directory path based on the algorithm and parameters
    results_dir = os.path.join(base_path, algorithm, param_dir)
    
    # Load results and average results
    results_path = os.path.join(results_dir, f"results_{arm_distribution}.csv")
    average_results_path = os.path.join(results_dir, f"average_results_{arm_distribution}.csv")

    # Check if the files exist in the parameter directory, otherwise check the default directory
    if not os.path.exists(results_path) or not os.path.exists(average_results_path):
        results_dir = os.path.join(base_path, algorithm, 'default')
        results_path = os.path.join(results_dir, f"results_{arm_distribution}.csv")
        average_results_path = os.path.join(results_dir, f"average_results_{arm_distribution}.csv")

    df_results = pd.read_csv(results_path)
    df_average = pd.read_csv(average_results_path)

    return df_results, df_average

# Layout of the Dash App
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
                                        # Checkbox for algorithm selection
                                        dcc.Checklist(
                                            id=f"{algo['value']}_{algo['index']}_checklist",
                                            options=[
                                                {"label": get_label_with_params(algo["value"], algo["params"]), 
                                                "value": f"{algo['value']}_{algo['index']}"}
                                            ],
                                            value=[f"{algo['value']}_{algo['index']}"],
                                            labelStyle={
                                                "color": algo["color"],
                                                'display': 'block',
                                                "margin-left": "20px" if "ETC" in algo["value"] or 
                                                                "Greedy" in algo["value"] or 
                                                                "UCB" in algo["value"] or 
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
                                # Dropdown for selecting first arm distribution
                                html.Label('Arm 1 Distribution', style={'margin-top': '10px'}),
                                dcc.Dropdown(
                                    id='arm_1_distribution',
                                    options=[{'label': f'{value}', 'value': f'{int(value * 1000)}'} for value in individual_arm_distribution],
                                    placeholder='Select Arm 1...',
                                    clearable=False,
                                    value='900',  # default value
                                    style={'margin-bottom': '10px'}
                                ),

                                # Dropdown for selecting second arm distribution
                                html.Label('Arm 2 Distribution', style={'margin-top': '10px'}),
                                dcc.Dropdown(
                                    id='arm_2_distribution',
                                    options=[{'label': f'{value}', 'value': f'{int(value * 1000)}'} for value in individual_arm_distribution],
                                    placeholder='Select Arm 2...',
                                    clearable=False,
                                    value='895',  # default value
                                    style={'margin-bottom': '10px'}
                                ),

                                # Dropdown for selecting third arm distribution (optional)
                                html.Label('Arm 3 Distribution (Optional)', style={'margin-top': '10px'}),
                                dcc.Dropdown(
                                    id='arm_3_distribution',
                                    options=[{'label': f'{value}', 'value': f'{int(value * 1000)}'} for value in individual_arm_distribution] + [{'label': '-', 'value': '-'}],
                                    placeholder='Select Arm 3 (Optional)...',
                                    clearable=True,
                                    value='-',  # default optional value
                                    style={'margin-bottom': '10px'}
                                ),
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
                                    options=[], 
                                    placeholder='Select...',
                                    clearable=False,
                                    value='None',
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
        ),
        # Placeholder for dynamically generated components
        html.Div(id='dynamic-content')
    ]
)

@app.callback(
    Output('selected_algorithm', 'options'),
    [Input(f"{algo['value']}_{algo['index']}_checklist", 'value') for algo in algorithm_data]
)
def update_dropdown_options(*selected_algorithms):
    # Flatten the list of selected algorithms
    selected_algorithms = [algo for algo_values in selected_algorithms for algo in algo_values]
    
    # Generate the new options for the dropdown
    new_options = [{'label': get_label_with_params(algo["value"], algo["params"]), 'value': f"{algo['value']}_{algo['index']}"} for algo in algorithm_data if f"{algo['value']}_{algo['index']}" in selected_algorithms]
    
    return new_options

# Callback for updating the plots
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure'),
     Output('plot5', 'figure'),
     Output('plot6', 'figure')], 
    [Input(f"{algo['value']}_{algo['index']}_checklist", 'value') for algo in algorithm_data] +
    [Input('selected_algorithm', 'value'),
     Input('alpha', 'value'),
     Input('arm_1_distribution', 'value'),
     Input('arm_2_distribution', 'value'),
     Input('arm_3_distribution', 'value')]
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
    selected_alpha = args[len(algorithm_data) + 1]
    arm_1 = args[len(algorithm_data) + 2]
    arm_2 = args[len(algorithm_data) + 3]
    arm_3 = args[len(algorithm_data) + 4]

    # Initialize empty figures
    fig1, fig2, fig3, fig4, fig5, fig6 = [go.Figure() for _ in range(6)]

    # Load data for each selected algorithm
    data = {}
    for algo in selected_algorithms:
        #data[algo] = load_data(algo, arm_distribution, first_move)
        data[algo] = load_data(algo, arm_1, arm_2, arm_3)

    # Plot 1: Average Total Reward
    fig1 = go.Figure()
    for algo in selected_algorithms:
        df = data[algo][1]
        algo_data = next((a for a in algorithm_data if a["value"] == algo.split('_')[0]), None)
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
        algo_data = next((a for a in algorithm_data if a["value"] == algo.split('_')[0]), None)
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
        algo_data = next((a for a in algorithm_data if a["value"] == algo.split('_')[0]), None)
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

    if selected_algorithm in selected_algorithms:
        selected_data = data[selected_algorithm][0]
        df_100k = selected_data[selected_data['Timestep'] == 100000]
        # Find the color for the selected algorithm
        selected_algo_info = next((algo for algo in algorithm_data if algo['value'] == selected_algorithm.split('_')[0]), None)
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
    else:
        fig4 = go.Figure()
        fig4.update_layout(
            title='Fig. 4: No data available',
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'color': 'black', "size": 8},
            showlegend=False
        )


    # Plot 5: Value at Risk Function
    alpha_value = float(selected_alpha)
    # Correctly format the arm distribution string for the VaR file
    if arm_3 == '-' or arm_3 is None:
        arm_distribution = f"{arm_1}_{arm_2}"
    else:
        arm_distribution = f"{arm_1}_{arm_2}_{arm_3}"
    
    
    fig5 = go.Figure()
    for algo in selected_algorithms:
        var_file = os.path.join(var_base_path, f"{algo.split('_')[0]}_VaR_{arm_distribution}_alpha_{alpha_value}.csv")
        if not os.path.exists(var_file):
            print(f"File not found: {var_file}")
            continue
        df_var = pd.read_csv(var_file)
        algo_data = next((a for a in algorithm_data if a["value"] == algo.split('_')[0]), None)
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
        algo_data = next((a for a in algorithm_data if a["value"] == algo.split('_')[0]), None)
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
