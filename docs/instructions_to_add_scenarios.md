# Instructions to adding Parameters to Vary Scenarios in `dashboard.py`

## Overview
This guide explains how to add parameters in the `dashboard.py` file to vary scenarios, such as adding different arm distributions and parameters depicted in new dropdown menus in the `app.layout`. It also discusses the necessary changes in the callback function and function inputs.

## Instructions

### 1. Generate Data with New Parameters
Update the algorithm scripts to include the new parameter in the filenames. For example, if you are saving results for different algorithms and arm distributions, modify the filename to reflect these parameters.

```python
# Example on how to rename the file to save the algorithm outout
algorithm.save_results_to_csv(f'{results_path}\{algorithm.name}_results_{first_move}_{arm_distribution}_{newparameter}.csv')
```

#### Step 1.1: Run Calculations for Dashboard
1. Navigate to the `../src/calculations_for_dashboard/calculate_averages.ipynb` file. Remember to rename the output file by adding the new parameter as a variable `{newparameter}` into the name.
2. Add your new algorithm to the corresponding group and rerun the notebook to update the averages.
3. Navigate to the `../src/calculations_for_dashboard/value_at_risk.ipynb` file. Remember to rename the output file by adding the new parameter as a variable `{newparameter}` into the name.
4. Add your new algorithm to the corresponding group and rerun the notebook to create the data visualized in plot 5.

### 2. Update `load_data` Function
Modify the `load_data` function in `dashboard.py` to access the changed filenames based on the new parameters.

```python
def load_data(algorithm, arm_distribution, first_move):

    results_path = os.path.join(base_path, f"{algorithm}_results_{first_move}_{arm_distribution}_{newparameter}.csv") # add {newparameter} here
    average_results_path = os.path.join(base_path, f"{algorithm}_average_results_{first_move}_{arm_distribution}_{newparameter}.csv") # add {newparameter} here

    df_results = pd.read_csv(results_path)
    df_average = pd.read_csv(average_results_path)

    return df_results, df_average
```

By following these steps, you can ensure that the data generation and loading processes in `dashboard.py` correctly handle the new parameters, allowing for more varied scenarios and accurate data retrieval.

### 3. Update `app.layout`
Add new dropdown menus to the layout to allow users to select different arm distributions and parameters.

```python
app.layout = html.Div(
                children[
                    # ... other components
                    html.Div([
                        dcc.Dropdown(
                                id='arm-distribution-dropdown',
                                options=[
                                        {'label': 'Uniform', 'value': 'uniform'},
                                        {'label': 'Normal', 'value': 'normal'},
                                        {'label': 'Bernoulli', 'value': 'bernoulli'}
                                        # you can also add other options in already existing components
                                ],
                                value='uniform'
                        ),
                        # ... other components
                    ])
                ]
            ),
```

### 4. Modify the Callback Function
Update the callback function to accept the new inputs from the dropdown menus and input fields.

```python
@app.callback(
        # other output components
        [ # oher input components
        Input('arm-distribution-dropdown', 'value')]
)
```

### 5. Update `update_plot` Function
Modify the `update_plot` function to include the new argument and the change of the file name in Plot 5.

```python
def update_plot(*args):
    
    # Extract the selected algorithms and parameters from the arguments
    selected_algorithms = [algo for algo_values in args[:len(algorithm_data)] for algo in algo_values]
    selected_algorithm = args[len(algorithm_data)]
    # other arguments...
    # add yours here

    # Initialize figures 

    # Plot 5
    # ...
    fig5 = go.Figure()
    for algo in selected_algorithms:
        var_file = os.path.join(var_base_path, f"{algo}_VaR_{first_move}_{arm_distribution}_{newparameter}_alpha_{alpha_value}.csv") # add {newparameter} here
        df_var = pd.read_csv(var_file)
    # ...

```

By following these steps, you can add parameters to the `dashboard.py` file to vary scenarios through new dropdown menus and input fields in the `app.layout`. The callback function and function inputs should be updated accordingly to handle the new parameters.


## Conclusion

By implementing the steps outlined in this guide, you can successfully add new parameters to your `dashboard.py` file, enabling more dynamic and varied scenarios in your application. This includes updating data generation scripts, modifying the `load_data` function, enhancing the `app.layout` with new dropdown menus, and adjusting the callback and `update_plot` functions to handle the new inputs. These changes will allow for a more flexible and comprehensive analysis of different algorithms and arm distributions, ultimately improving the functionality and user experience of your dashboard.