import os
"""
This script calculates the Value at Risk (VaR) for different algorithms and their configurations over multiple timesteps.
It reads results from CSV files, computes the VaR for specified alpha values, and saves the results to new CSV files.
Functions:
    calculate_value_at_risk(df, alpha):
        Calculates the Value at Risk (VaR) for a given DataFrame and alpha value.
    calculate_var_for_algorithms(algorithm_strategy_pairs, combinations, alpha_values, base_path, output_path):
        Calculates the VaR for individual algorithms and saves the results to CSV files.
    run_value_at_risk(algorithm_data, algorithm_groups, combinations, alpha_values, base_path, output_path):
        Orchestrates the calculation of VaR for individual algorithms and algorithm groups.
Usage:
    This script is intended to be run directly. When executed, it adjusts the sys.path to include the parent directory
    and then performs the VaR calculations for the specified algorithms and configurations.
"""
import sys
import pandas as pd

# Adjust the sys.path to include the parent directory when the script is run directly
if __name__ == "__main__" and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_script import get_directory_for_algorithm, algorithm_strategy_pairs, base_path, output_path, combinations, alpha_values, algorithm_groups

def calculate_value_at_risk(df, alpha):
    timesteps = df['Timestep'].unique()
    return [df[df['Timestep'] == t]['Total Regret'].quantile(1 - alpha) for t in timesteps]

def calculate_var_for_algorithms(algorithm_strategy_pairs, combinations, alpha_values, base_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for algo, config in algorithm_strategy_pairs:
        for arm_means, combination_name in combinations:
            # Get the directory for this algorithm and strategy
            results_dir = get_directory_for_algorithm(algo, config["params"])
            
            results_path = os.path.join(results_dir, f"results_{combination_name}.csv")
            if not os.path.exists(results_path):
                print(f"File not found: {results_path}")
                continue
            df = pd.read_csv(results_path)
            
            for alpha in alpha_values:
                var_values = calculate_value_at_risk(df, alpha)
                output_file = os.path.join(output_path, f"{algo.name}_VaR_{combination_name}_alpha_{alpha}.csv")
                pd.DataFrame({
                    'Timestep': df['Timestep'].unique(),
                    'Value_at_Risk': var_values
                }).to_csv(output_file, index=False)

def run_value_at_risk(algorithm_data, algorithm_groups, combinations, alpha_values, base_path, output_path):
    # Step 1: Calculate VaR for individual algorithms
    calculate_var_for_algorithms(algorithm_data, combinations, alpha_values, base_path, output_path)

    # Step 2: Calculate VaR for algorithm groups
    #calculate_average_var_and_save(algorithm_groups, combinations, alpha_values, output_path)


if __name__ == "__main__":
    # Example data for running the script
    #algorithm_data = algorithm_strategy_pairs
    #algorithm_groups = []  # Define your algorithm groups if needed

    run_value_at_risk(algorithm_strategy_pairs, algorithm_groups, combinations, alpha_values, base_path, output_path)