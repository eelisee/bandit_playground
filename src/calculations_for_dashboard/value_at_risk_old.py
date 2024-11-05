import os
import pandas as pd
import sys

# Adjust the sys.path to include the parent directory when the script is run directly
if __name__ == "__main__" and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_script import get_directory_for_algorithm, algorithm_strategy_pairs, output_path


def calculate_value_at_risk(df, alpha):
    timesteps = df['Timestep'].unique()
    return [df[df['Timestep'] == t]['Total Regret'].quantile(1 - alpha) for t in timesteps]

def calculate_var_for_algorithms(algorithm_strategy_pairs, combinations, alpha_values, base_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for algo, config in algorithm_strategy_pairs:
        for combination in combinations:
            # Get the directory for this algorithm and strategy
            results_dir = get_directory_for_algorithm(algo, config["params"])
            
            results_path = os.path.join(results_dir, f"results_{combination}.csv")
            if not os.path.exists(results_path):
                print(f"File not found: {results_path}")
                continue
            df = pd.read_csv(results_path)
            
            for alpha in alpha_values:
                var_values = calculate_value_at_risk(df, alpha)
                output_file = os.path.join(output_path, f"{algo.name}_VaR_{combination}_alpha_{alpha}.csv")
                pd.DataFrame({
                    'Timestep': df['Timestep'].unique(),
                    'Value_at_Risk': var_values
                }).to_csv(output_file, index=False)

# def calculate_average_var_and_save(algorithms_groups, combinations, alpha_values, output_path):
#     for group_name, algorithms in algorithms_groups.items():
#         for combination in combinations:
#             combined_df = None

#             for alpha in alpha_values:
#                 for algorithm in algorithms:
#                     file_path = os.path.join(output_path, f"{algorithm}_VaR_{combination}_alpha_{alpha}.csv")
#                     df = pd.read_csv(file_path)

#                     if combined_df is None:
#                         combined_df = df
#                     else:
#                         combined_df.iloc[:, 1:] += df.iloc[:, 1:]  # Sum up values

#                 combined_df.iloc[:, 1:] /= len(algorithms)  # Calculate average

#                 output_file_path = os.path.join(output_path, f"{group_name}_VaR_{combination}_alpha_{alpha}.csv")
#                 combined_df.to_csv(output_file_path, index=False)

def run_value_at_risk(algorithm_data, algorithm_groups, combinations, alpha_values, base_path, output_path):
    # Step 1: Calculate VaR for individual algorithms
    calculate_var_for_algorithms(algorithm_data, combinations, alpha_values, base_path, output_path)

    # Step 2: Calculate VaR for algorithm groups
    #calculate_average_var_and_save(algorithm_groups, combinations, alpha_values, output_path)