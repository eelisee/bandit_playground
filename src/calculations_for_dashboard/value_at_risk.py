import os
import pandas as pd
import sys

# Base path
base_path = os.path.abspath(os.path.join(os.getcwd(), "data", "algorithms_results"))
output_path = os.path.abspath(os.path.join(base_path, "Value_at_Risk"))

# Classification of algorithms
var_aware_algorithms = ["UCB-Tuned", "UCB-V", "EUCBV"]
not_var_aware_algorithms = []# "PAC-UCB", "UCB-Improved"]
standard_algorithms = []#"ETC", "Greedy", "UCB", "UCB-Normal"]
def calculate_average_var_and_save(algorithms, group_name):
    all_var_values = []
    for algo in algorithms:
        for i, arm_means in enumerate(unique_arm_combinations):
            version = f'ver{i+1}'
            for j in range(2):
                if j == 1:
                    arm_means = arm_means[::-1]
                opt_subopt = 'opt' if arm_means[0] > arm_means[1] else 'subopt'
                combination = f"{opt_subopt}_{version}"

                for alpha in alpha_values:
                    var_file = os.path.join(output_path, f"{algo}_VaR_{combination}_alpha_{alpha}.csv")
                    df_var = pd.read_csv(var_file)
                    all_var_values.append(df_var['Value_at_Risk'].values)

    if all_var_values:
        avg_var_values = pd.DataFrame(all_var_values).mean(axis=0)
        avg_var_df = pd.DataFrame({
            'Timestep': df_var['Timestep'].unique(),
            'Average_Value_at_Risk': avg_var_values
        })
        avg_var_df.to_csv(os.path.join(output_path, f"{group_name}_Average_VaR.csv"), index=False)

calculate_average_var_and_save(var_aware_algorithms, "Variance-aware UCB Variations")
calculate_average_var_and_save(not_var_aware_algorithms, "Not-variance-aware UCB Variations")
calculate_average_var_and_save(standard_algorithms, "Standard Algorithms")

algorithm_data = var_aware_algorithms + not_var_aware_algorithms + standard_algorithms

# Unique arm combinations
unique_arm_combinations = [
    [0.9, 0.8],
    [0.9, 0.895],
    [0.5, 0.495]
]

# Alpha values for VaR calculation
alpha_values = [0.01, 0.05, 0.1]

# Calculate VaR for each time step
def calculate_value_at_risk(df, alpha):
    timesteps = df['Timestep'].unique()
    return [df[df['Timestep'] == t]['Total Regret'].quantile(1 - alpha) for t in timesteps]

def main():
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for algo in algorithm_data:
        for i, arm_means in enumerate(unique_arm_combinations):
            version = f'ver{i+1}'
            for j in range(2):
                if j == 1:
                    arm_means = arm_means[::-1]
                opt_subopt = 'opt' if arm_means[0] > arm_means[1] else 'subopt'
                combination = f"{opt_subopt}_{version}"

                results_path = os.path.join(base_path, f"{algo}_results_{combination}.csv")
                df = pd.read_csv(results_path)
                
                for alpha in alpha_values:
                    var_values = calculate_value_at_risk(df, alpha)
                    output_file = os.path.join(output_path, f"{algo}_VaR_{combination}_alpha_{alpha}.csv")
                    pd.DataFrame({
                        'Timestep': df['Timestep'].unique(),
                        'Value_at_Risk': var_values
                    }).to_csv(output_file, index=False)
    
        # Calculate average VaR for each group of algorithms

    print("Value at Risk successfully calculated.")

if __name__ == "__main__":
    main()