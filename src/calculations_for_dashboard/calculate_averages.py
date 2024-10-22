import sys
import os
import pandas as pd

# Classification of algorithms
var_aware_algorithms = ["UCB-Tuned", "UCB-V", "EUCBV"]
not_var_aware_algorithms = []# "PAC-UCB", "UCB-Improved"]
standard_algorithms = []#"ETC", "Greedy", "UCB", "UCB-Normal"]

# Base path
base_path = os.path.abspath(os.path.join(os.getcwd(), "data", "algorithms_results"))

# Unique arm combinations
unique_arm_combinations = [
    [0.9, 0.8],
    [0.9, 0.895],
    [0.5, 0.495]
]

# Function to calculate the average and save the results
def calculate_average_and_save(algorithms, output_file_suffix):
    for i, arm_means in enumerate(unique_arm_combinations):
        version = f'ver{i+1}'
        for j in range(2):
            if j == 1:
                arm_means = arm_means[::-1]  # Interchange first and second value
            opt_subopt = 'opt' if arm_means[0] > arm_means[1] else 'subopt'
            combination = f"{opt_subopt}_{version}"

            combined_df = None

            for algorithm in algorithms:
                file_path = os.path.join(base_path, f"{algorithm}_results_{combination}.csv")
                df = pd.read_csv(file_path)

                if combined_df is None:
                    combined_df = df
                else:
                    combined_df.iloc[:, 1:] += df.iloc[:, 1:]  # Add the values of the respective columns

            combined_df.iloc[:, 1:] /= len(algorithms)  # Calculate the average

            output_file_path = os.path.join(base_path, f"{output_file_suffix}_results_{combination}.csv")
            combined_df.to_csv(output_file_path, index=False)

# Run the averaging for different groups of algorithms
def main():
    # Calculate and save the averages for variance-aware algorithms
    calculate_average_and_save(var_aware_algorithms, "Variance-aware UCB Variations")
    
    # Calculate and save the averages for not variance-aware algorithms
    calculate_average_and_save(not_var_aware_algorithms, "Not-variance-aware UCB Variations")
    
    # Calculate and save the averages for standard algorithms
    calculate_average_and_save(standard_algorithms, "Standard Algorithms")

    print("Averages successfully calculated and saved.")

if __name__ == "__main__":
    main()