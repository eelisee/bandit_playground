import numpy as np
import os
import csv
import signal
import sys
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor

from utils.bandit_algorithm import BanditAlgorithm
from utils.simulation_utils import general_simulation
from utils.combination import generate_combinations_copy
#from calculations_for_dashboard.value_at_risk import run_value_at_risk
#from calculations_for_dashboard.calculate_averages import run_average_calculations
#from calculations_for_dashboard.calculate_averages import main as calculate_averages_main

# Import simulation functions for each algorithm
from algorithms.ETC import ETC_simulation
from algorithms.Greedy import Greedy_simulation
from algorithms.UCB import UCB_simulation
#from algorithms.UCB_Normal import UCB_Normal_simulation
from algorithms.UCB_Tuned import UCB_Tuned_simulation
from algorithms.UCB_V import UCB_V_simulation
from algorithms.PAC_UCB import PAC_UCB_simulation
from algorithms.UCB_Improved import UCB_Improved_simulation
from algorithms.EUCBV import EUCBV_simulation

# Parameters
time_horizons = [2, 3, 100, 200, 2000, 10000, 20000, 40000, 60000, 80000, 10000] #, 200000, 400000, 600000, 800000, 1000000]

# List of algorithms and their corresponding strategies
algorithm_strategy_pairs = [
    # (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 10}}),
    # (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 100}}),
    # (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 1000}}),
    # (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 10000}}),
    # (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 100000}}),
    # (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.005}}),
    # (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.01}}),
    # (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.05}}),
    # (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.1}}),
    # (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.5}}),
    # (BanditAlgorithm("UCB"), {"strategy_fn": UCB_simulation, "params": {}}),
    # #(BanditAlgorithm("UCB-Normal"), {"strategy_fn": UCB_Normal_simulation, "params": {"arm_variances": np.array([0.249975, 0.25])}}), # nicht möglich für arm_variance (algorithmus anders implementieren)
    # (BanditAlgorithm("UCB-Tuned"), {"strategy_fn": UCB_Tuned_simulation, "params": {}}),
    # (BanditAlgorithm("UCB-V"), {"strategy_fn": UCB_V_simulation, "params": {"theta": 1, "c": 1, "b": 1}}),
    # (BanditAlgorithm("PAC-UCB"), {"strategy_fn": PAC_UCB_simulation, "params": {"c": 1, "b": 1, "q": 1.3, "beta": 0.05}}),
    # (BanditAlgorithm("UCB-Improved"), {"strategy_fn": UCB_Improved_simulation, "params": {"delta": 1}}),
    # (BanditAlgorithm("EUCBV"), {"strategy_fn": EUCBV_simulation, "params": {"rho": 0.5}})
    (BanditAlgorithm("UCB-V"), {"strategy_fn": UCB_V_simulation, "params": {"theta": 1, "c": 1, "b": 1, "variance": 0.1}}),
    (BanditAlgorithm("UCB-V"), {"strategy_fn": UCB_V_simulation, "params": {"theta": 1, "c": 1, "b": 1, "variance": 0.5}}),
    (BanditAlgorithm("UCB-V"), {"strategy_fn": UCB_V_simulation, "params": {"theta": 1, "c": 1, "b": 1, "variance": 1}}),
    (BanditAlgorithm("UCB-V"), {"strategy_fn": UCB_V_simulation, "params": {"theta": 1, "c": 1, "b": 1, "variance": 10}})
]

# Algorithm group definitions, add algorithms to the respective groups here
algorithm_groups = {
    "Variance-aware UCB Variations": ["UCB-V"]#,["UCB-Tuned", "UCB-V", "EUCBV"],
    # "Not-variance-aware UCB Variations": ["PAC-UCB", "UCB-Improved"],
    # "Standard Algorithms": ["ETC", "Greedy", "UCB"]
}

# Define alpha values
alpha_values = [0.01, 0.05, 0.1]

# Define the possible individual arm values
individual_arm_distribution = [0.9, 0.895, 0.89, 0.85, 0.8]

################ do not modify below this line ##################

# Signal handler for graceful shutdown on Ctrl + C
def signal_handler(sig, frame):
    print("\nTerminating processes...")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Generate the combinations
combinations = generate_combinations_copy(individual_arm_distribution)

# Base paths
base_path = os.path.join(os.getcwd(), 'data', 'algorithms_results')
output_path = os.path.join(base_path, "Value_at_Risk")


# Algorithm names
algorithms = [alg.name for alg, _ in algorithm_strategy_pairs]

# Ensure directories are created before saving results
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Create directory based on algorithm name and parameters
def get_directory_for_algorithm(algorithm, params):
    algorithm_dir = os.path.join(base_path, algorithm.name)

    # Dynamically generate parameter directory by iterating over params
    if params:
        param_dir = '_'.join(['{}_{}'.format(key, str(value).replace('.', '_')) for key, value in params.items()])
    else:
        param_dir = 'default'
    
    # Construct full directory path and create it if necessary
    full_dir = os.path.join(algorithm_dir, param_dir)
    create_directory(full_dir)
    
    return full_dir

# Perform simulation and save results for each algorithm
def run_simulation_inner(algorithm, strategy, arm_means, combination_name, time_horizons):
    print(f"Running simulation for {algorithm.name} with arm means {arm_means} and strategy {strategy['strategy_fn'].__name__}")

    # Get the directory for this algorithm and strategy
    results_dir = get_directory_for_algorithm(algorithm, strategy["params"])

    # Check if the results for this combination already exist
    detailed_results_path = os.path.join(results_dir, f'results_{combination_name}.csv')
    if os.path.exists(detailed_results_path):
        print(f"Results for {algorithm.name} with combination {combination_name} already exist. Skipping simulation.")
        return

    # Run the simulation
    general_simulation(algorithm, arm_means, time_horizons, strategy["strategy_fn"], **strategy["params"])

    # Save detailed results to CSV
    algorithm.save_results_to_csv(detailed_results_path)
    print(f"Saved detailed results to {detailed_results_path}")

    # Calculate and save average results to CSV
    avg_results = algorithm.calculate_average_results()
    avg_results_path = os.path.join(results_dir, f'average_results_{combination_name}.csv')
    save_average_results(avg_results, avg_results_path)

    # Get the directory for this algorithm and strategy
    results_dir = get_directory_for_algorithm(algorithm, strategy["params"])

    # Save detailed results to CSV
    detailed_results_path = os.path.join(results_dir, f'results_{combination_name}.csv')
    algorithm.save_results_to_csv(detailed_results_path)
    print(f"Saved detailed results to {detailed_results_path}")

    # Calculate and save average results to CSV
    avg_results = algorithm.calculate_average_results()
    avg_results_path = os.path.join(results_dir, f'average_results_{combination_name}.csv')
    save_average_results(avg_results, avg_results_path)

def run_simulation(algorithm, strategy, combinations, time_horizons):
    with ProcessPoolExecutor(max_workers=None) as executor_inner:
        futures_inner = [
            executor_inner.submit(run_simulation_inner, algorithm, strategy, arm_means, combination_name, time_horizons)
            for arm_means, combination_name in combinations
        ]
        for future_inner in futures_inner:
            future_inner.result()

def save_average_results(avg_results, path):
    """
    Save the average results to a CSV file.
    """
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestep', 'Average Total Reward', 'Average Suboptimal Arms', 'Average Regret', 'Average Zeros Count', 'Average Ones Count'])
        for result in avg_results:
            writer.writerow(result)
    print(f"Saved average results to {path}")

if __name__ == '__main__':
    # Get number of CPU cores available
    num_cores = os.cpu_count()
    
    # Use all cores, or adjust based on memory availability (e.g., use 75% of cores)
    max_workers = int(num_cores * 0.75)

    try:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(run_simulation, algorithm, strategy, combinations, time_horizons)
                for algorithm, strategy in algorithm_strategy_pairs
            ]
            for future in futures:
                future.result()
    except KeyboardInterrupt:
        print("Execution stopped by user.")

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