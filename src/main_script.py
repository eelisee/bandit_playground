import numpy as np
import os
import csv
from utils.bandit_algorithm import BanditAlgorithm
from utils.simulation_utils import general_simulation
from algorithms.ETC import ETC_simulation
#from algorithms.Greedy import Greedy_simulation
#from algorithms.UCB import UCB_simulation
#from algorithms.UCB_Normal import UCB_Normal_simulation
from algorithms.UCB_Tuned import UCB_Tuned_simulation
from algorithms.UCB_V import UCB_V_simulation
#from algorithms.PAC_UCB import PAC_UCB_simulation
#from algorithms.UCB_Improved import UCB_Improved_simulation
from algorithms.EUCBV import EUCBV_simulation

# Parameters
time_horizons = [2, 3, 100, 200, 2000, 10000, 20000, 40000, 60000, 80000, 100000]

# List of algorithms and their corresponding strategies
algorithm_strategy_pairs = [
    # (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 1000}}),
    # (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.05}}),
    # (BanditAlgorithm("UCB"), {"strategy_fn": UCB_simulation, "params": {}}),
    # (BanditAlgorithm("UCB-Normal"), {"strategy_fn": UCB_Normal_simulation, "params": {"arm_variances": np.array([0.249975, 0.25])}}),
    (BanditAlgorithm("UCB-Tuned"), {"strategy_fn": UCB_Tuned_simulation, "params": {}}),
    (BanditAlgorithm("UCB-V"), {"strategy_fn": UCB_V_simulation, "params": {"theta": 1, "c": 1, "b": 1}}),
    # (BanditAlgorithm("PAC-UCB"), {"strategy_fn": PAC_UCB_simulation, "params": {"c": 1, "b": 1, "q": 1.3, "beta": 0.05}}),
    # (BanditAlgorithm("UCB-Improved"), {"strategy_fn": UCB_Improved_simulation, "params": {"delta": 1}}),
    (BanditAlgorithm("EUCBV"), {"strategy_fn": EUCBV_simulation, "params": {"rho": 0.5}})
]

# Results path
results_path = r'/Users/canis/Documents/coding/bandit_playground/data/algorithms_results'
if not os.path.exists(results_path):
    os.makedirs(results_path)  # Ensure directory exists
    print(f"Created directory: {results_path}")

# Unique arm combinations
unique_arm_combinations = [
    np.array([0.9, 0.8]),
    np.array([0.9, 0.895]),
    np.array([0.5, 0.495])
]

# Perform simulation and save results for each algorithm
for algorithm, strategy in algorithm_strategy_pairs:
    for i, arm_means in enumerate(unique_arm_combinations):
        version = f'ver{i+1}'
        for j in range(2):
            if j == 1:
                arm_means = arm_means[::-1]  # Interchange first and second value
            opt_subopt = 'opt' if arm_means[0] > arm_means[1] else 'subopt'

            print(f"Running simulation for {algorithm.name} with arm means {arm_means} and strategy {strategy['strategy_fn'].__name__}")
            general_simulation(algorithm, arm_means, time_horizons, strategy["strategy_fn"], **strategy["params"])

            # Save detailed results to CSV
            detailed_results_path = f'{results_path}/{algorithm.name}_results_{opt_subopt}_{version}.csv'
            algorithm.save_results_to_csv(detailed_results_path)
            print(f"Saved detailed results to {detailed_results_path}")

            # Calculate and save average results to CSV
            avg_results = algorithm.calculate_average_results()
            avg_results_path = f'{results_path}/{algorithm.name}_average_results_{opt_subopt}_{version}.csv'
            with open(avg_results_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestep', 'Average Total Reward', 'Average Suboptimal Arms', 'Average Regret', 'Average Zeros Count', 'Average Ones Count'])
                for result in avg_results:
                    writer.writerow(result)
            print(f"Saved average results to {avg_results_path}")