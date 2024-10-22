import numpy as np
import os
import csv
from itertools import permutations
from utils.bandit_algorithm import BanditAlgorithm
from utils.simulation_utils import general_simulation
#from calculations_for_dashboard.value_at_risk import run_value_at_risk
#from calculations_for_dashboard.calculate_averages import run_average_calculations
#from calculations_for_dashboard.calculate_averages import main as calculate_averages_main



# Import simulation functions for each algorithm
from algorithms.ETC import ETC_simulation
from algorithms.Greedy import Greedy_simulation
from algorithms.UCB import UCB_simulation
from algorithms.UCB_Normal import UCB_Normal_simulation
from algorithms.UCB_Tuned import UCB_Tuned_simulation
from algorithms.UCB_V import UCB_V_simulation
from algorithms.PAC_UCB import PAC_UCB_simulation
from algorithms.UCB_Improved import UCB_Improved_simulation
from algorithms.EUCBV import EUCBV_simulation

# Parameters
time_horizons = [2, 3, 100, 200, 2000, 10000, 20000, 40000, 60000, 80000, 100000]
time_horizons = [2, 3, 100] #, 200, 2000, 10000, 20000, 40000, 60000, 80000, 100000]

# List of algorithms and their corresponding strategies
algorithm_strategy_pairs = [
    (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 1000}}),
    (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.05}}),
    (BanditAlgorithm("UCB"), {"strategy_fn": UCB_simulation, "params": {}}),
    #(BanditAlgorithm("UCB-Normal"), {"strategy_fn": UCB_Normal_simulation, "params": {"arm_variances": np.array([0.249975, 0.25])}}),
    (BanditAlgorithm("UCB-Tuned"), {"strategy_fn": UCB_Tuned_simulation, "params": {}}),
    (BanditAlgorithm("UCB-V"), {"strategy_fn": UCB_V_simulation, "params": {"theta": 1, "c": 1, "b": 1}}),
    (BanditAlgorithm("PAC-UCB"), {"strategy_fn": PAC_UCB_simulation, "params": {"c": 1, "b": 1, "q": 1.3, "beta": 0.05}}),
    (BanditAlgorithm("UCB-Improved"), {"strategy_fn": UCB_Improved_simulation, "params": {"delta": 1}}),
    (BanditAlgorithm("EUCBV"), {"strategy_fn": EUCBV_simulation, "params": {"rho": 0.5}})
]

# Algorithm names
algorithms = [alg.name for alg, _ in algorithm_strategy_pairs]

# Algorithm group definitions, add algorithms to the respective groups here
algorithm_groups = {
    "Variance-aware UCB Variations": ["UCB-Tuned", "UCB-V", "EUCBV"],
    "Not-variance-aware UCB Variations": ["PAC-UCB", "UCB-Improved"],
    "Standard Algorithms": ["ETC", "Greedy", "UCB"]
}

# Unique arm combinations
unique_arm_combinations = [
    np.array([0.9, 0.8, 0.7]),
    np.array([0.9, 0.85, 0.8]),
    np.array([0.9, 0.8]),
    #np.array([0.9, 0.895]),
    #np.array([0.5, 0.495])
]

# Define alpha values
alpha_values = [0.01, 0.05, 0.1]

# def generate_combinations(unique_arm_combinations):
#     combinations = []
#     for i, arm_means in enumerate(unique_arm_combinations):
#         for j in range(2):
#             if j == 1:
#                 arm_means = arm_means[::-1]  # Interchange first and second value
#             opt_subopt = 'opt' if arm_means[0] > arm_means[1] else 'subopt'
#             combinations.append(f"{opt_subopt}_ver{i+1}")
#     return combinations

# combinations = generate_combinations(unique_arm_combinations)

# Generate permutations of the arms, handling both 2-arm and 3-arm combinations
def generate_combinations(unique_arm_combinations):
    combinations = []
    for arm_means in unique_arm_combinations:
        # Generate all permutations for each arm set
        perms = permutations(arm_means)
        for perm in perms:
            # Convert arm values to percentages for naming
            combination_name = "_".join(str(int(a * 1000) if a < 1 else int(a * 100)) for a in perm)  
            combinations.append((perm, combination_name))
    return combinations

combinations = generate_combinations(unique_arm_combinations)

# Base paths
base_path = os.path.join(os.getcwd(), 'data', 'algorithms_results')
output_path = os.path.join(base_path, "Value_at_Risk")

# # Perform simulation and save results for each algorithm
# for algorithm, strategy in algorithm_strategy_pairs:
#     for i, arm_means in enumerate(unique_arm_combinations):
#         version = f'ver{i+1}'
#         for j in range(2):
#             if j == 1:
#                 arm_means = arm_means[::-1]  # Interchange first and second value
#             opt_subopt = 'opt' if arm_means[0] > arm_means[1] else 'subopt'

#             print(f"Running simulation for {algorithm.name} with arm means {arm_means} and strategy {strategy['strategy_fn'].__name__}")
#             general_simulation(algorithm, arm_means, time_horizons, strategy["strategy_fn"], **strategy["params"])

#             # Save detailed results to CSV
#             detailed_results_path = f'{base_path}/{algorithm.name}_results_{opt_subopt}_ver{i+1}.csv'
#             algorithm.save_results_to_csv(detailed_results_path)
#             print(f"Saved detailed results to {detailed_results_path}")

#             # Calculate and save average results to CSV
#             avg_results = algorithm.calculate_average_results()
#             avg_results_path = f'{base_path}/{algorithm.name}_average_results_{opt_subopt}_ver{i+1}.csv'
#             with open(avg_results_path, mode='w', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(['Timestep', 'Average Total Reward', 'Average Suboptimal Arms', 'Average Regret', 'Average Zeros Count', 'Average Ones Count'])
#                 for result in avg_results:
#                     writer.writerow(result)
#             print(f"Saved average results to {avg_results_path}")

# Perform simulation and save results for each algorithm
for algorithm, strategy in algorithm_strategy_pairs:
    for arm_means, combination_name in combinations:
        print(f"Running simulation for {algorithm.name} with arm means {arm_means} and strategy {strategy['strategy_fn'].__name__}")
        
        # Run the simulation
        general_simulation(algorithm, arm_means, time_horizons, strategy["strategy_fn"], **strategy["params"])

        # Save detailed results to CSV
        detailed_results_path = f'{base_path}/{algorithm.name}_results_{combination_name}.csv'
        algorithm.save_results_to_csv(detailed_results_path)
        print(f"Saved detailed results to {detailed_results_path}")

        # Calculate and save average results to CSV
        avg_results = algorithm.calculate_average_results()
        avg_results_path = f'{base_path}/{algorithm.name}_average_results_{combination_name}.csv'
        with open(avg_results_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestep', 'Average Total Reward', 'Average Suboptimal Arms', 'Average Regret', 'Average Zeros Count', 'Average Ones Count'])
            for result in avg_results:
                writer.writerow(result)
        print(f"Saved average results to {avg_results_path}")

# # Run average calculations
# run_average_calculations(algorithm_groups, combinations, base_path)

# # Call the Value at Risk calculation function
# run_value_at_risk(algorithms, algorithm_groups, combinations, alpha_values, base_path, output_path)

# Run average calculations
#run_average_calculations(algorithm_groups, [comb[1] for comb in combinations], base_path)

# Other parts of your script here

# Call the averaging process for all algorithms
#calculate_averages_main()

# Call the Value at Risk calculation function
#run_value_at_risk(algorithms, algorithm_groups, [comb[1] for comb in combinations], alpha_values, base_path, output_path)