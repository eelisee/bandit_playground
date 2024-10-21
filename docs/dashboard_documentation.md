# Dashboard Documentation

## Overview
This document provides detailed instructions on how to modify and extend the dashboard, specifically focusing on adding new plots.

## Adding New Plots

### Step 1: Define the New Plot
First, you need to define the new plot in the `update_plots` function in `src/dashboard.py`. For example, if you want to add a new plot showing the cumulative reward over time, you might add something like this:

```python
def update_plots(*args):
    # Existing plot definitions...

    # New plot definition
    fig7 = go.Figure()
    for algo in selected_algorithms:
        df = data[algo][1]
        algo_data = next((a for a in algorithm_data if a["value"] == algo), None)
        if algo_data: 
            fig7.add_trace(go.Scatter(
                x=timesteps, # set x-axis value
                y=df[cumulative_rewards], # refer to the calculation of the cumulative reward that you've added to the data e.g. in `/src/calculations_for_dashboard`
                mode='lines+markers', # add your description here
                name='Cumulative Reward', # add your description here
                line=dict(color=algo_data["color"], dash=algo_data["line_style"]) 
            ))
    fig7.update_layout(
        title="Cumulative Reward Over Time", # define
        xaxis_title="Timesteps", # define
        yaxis_title="Cumulative Reward", # define
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': 'black', "size": 8},
        showlegend=False
    )

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7 # add new figure here
```


Step 2: Update the Layout
Next, you need to update the layout of the dashboard to include the new plot. This involves modifying the layout section of the Dash app to add a new dcc.Graph component for the new plot.

app.layout = html.Div([
    # Existing layout components...

    # New plot component
    dcc.Graph(id='cumulative-reward-plot', figure=fig7)
])

Step 3: Update the Callback
Ensure that the callback function that updates the plots includes the new plot. Modify the callback to return the new figure.

@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure'),
     Output('plot5', 'figure'),
     Output('plot6', 'figure'),
     Output('cumulative-reward-plot', 'figure')],
    [Input('some-input', 'value')]
)
def update_output(value):
    # Existing plot updates...

    fig7 = update_plots(value)[6]  # Assuming fig7 is the 7th plot

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7

Step 4: Test the New Plot
Finally, run the dashboard and verify that the new plot appears as expected.

python [dashboard.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22%2FUsers%2Fcanis%2FDocuments%2Fcoding%2Fbandit_playground%2Fsrc%2Fdashboard.py%22%2C%22path%22%3A%22%2FUsers%2Fcanis%2FDocuments%2Fcoding%2Fbandit_playground%2Fsrc%2Fdashboard.py%22%2C%22scheme%22%3A%22file%22%7D%7D)

Open your browser and go to http://127.0.0.1:8050 to see the new plot in action.

Conclusion
By following these steps, you can add new plots to the dashboard, enhancing its functionality and providing more insights into the performance of the algorithms.

For further details on adding new algorithms and generating data for the plots, refer to the setup_instructions.md file.


This file provides a clear and detailed guide on how to add new plots to the dashboard, making it easier for other developers to extend its functionality.