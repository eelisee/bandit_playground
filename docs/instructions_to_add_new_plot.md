# Instructions to add new Plot

## Overview
This document provides detailed instructions on how to modify and extend the dashboard, specifically focusing on adding new plots.

## Instructions

### Step 1: Add a New Branch
Before making any changes, create a new branch for your work:
```sh
git checkout -b add-new-plot
```

### Step 2: Define the New Plot
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

### Step 3: Update the Layout
Next, you need to update the layout of the dashboard to include the new plot. This involves modifying the layout section of the Dash app to add a new dcc.Graph component for the new plot.

```python
app.layout = html.Div([
    # Existing layout components...

    # New plot component
    html.Div(style={'flex': '1 1 30%', 'padding': '10px'}, children=[dcc.Graph(id='plot7')]) # add
])
```

### Step 4: Update the Callback
Ensure that the callback function that updates the plots includes the new plot. Modify the callback to return the new figure.

```python
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure'),
     Output('plot5', 'figure'),
     Output('plot6', 'figure'),
     Output('plot7', 'figure')], # add
    [Input('some-input', 'value')]
)
```

### Step 5: Test the New Plot
Finally, run the dashboard and verify that the new plot appears as expected.

```bash
python src/dashboard.py
```

Open your browser and go to http://127.0.0.1:8050 to see the new plot in action.

### (Additional) Step 6: Write Unit Tests
1. Navigate to the `tests` directory.
2. Create a new test file for your algorithm, e.g., `test_new_algorithm.py`.
3. Write unit tests to verify the correctness of your algorithm. Ensure you cover various edge cases.

### Step 7: Update Documentation
1. Navigate to the `docs` directory.
2. Update the documentation file `documentation.md` to include information about your new algorithm.
3. Ensure you provide a detailed description, usage examples, and any necessary diagrams or illustrations.

### Step 8: Commit and Push Changes
1. Add your changes to the staging area:
    ```sh
    git add .
    ```
2. Commit your changes with a descriptive message:
    ```sh
    git commit -m "Add new algorithm (and corresponding tests)"
    ```
3. Push your changes to the remote repository:
    ```sh
    git push origin add-new-algorithm
    ```

### Step 9: Create a Pull Request
1. Go to the repository on GitHub.
2. Create a new pull request from your branch.
3. Provide a detailed description of your changes and request a review.

### Step 10: Address Review Feedback
1. Address any feedback provided by reviewers.
2. Make necessary changes and push them to your branch.
3. Once approved, merge your pull request.

## Conclusion
By following these steps, you can add new plots to the dashboard, enhancing its functionality and providing more insights into the performance of the algorithms. For further details on adding new algorithms and generating data for the plots, refer to the other instruction files.
