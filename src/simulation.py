import numpy as np
import os
import csv
import signal
import sys
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor

from config import algorithm_strategy_pairs,algorithm_groups, time_horizons, combinations, alpha_values, global_seed, base_path
from utils.simulation_utils import general_simulation, get_directory_for_algorithm
from calculations_for_dashboard.value_at_risk import run_value_at_risk


################ do not modify ##################

# Signal handler for graceful shutdown on Ctrl + C
def signal_handler(sig, frame):
    #print("\nTerminating processes...")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Algorithm names
algorithms = [alg.name for alg, _ in algorithm_strategy_pairs]

# Perform simulation and save results for each algorithm
def run_simulation_inner(algorithm, strategy, arm_means, combination_name, time_horizons, seed=global_seed):
    print(f"Running simulation for {algorithm.name} with arm means {arm_means} and strategy {strategy['strategy_fn'].__name__}")

    # Set the random seed for reproducibility
    rng = np.random.default_rng(seed)

    # Get the directory for this algorithm and strategy
    results_dir = get_directory_for_algorithm(algorithm, strategy["params"])

    # Check if the results for this combination already exist
    detailed_results_path = os.path.join(results_dir, f'results_{combination_name}.csv')
    if os.path.exists(detailed_results_path):
        print(f"Results for {algorithm.name} with combination {combination_name} already exist. Skipping simulation.")
        return

    # Run the simulation
    general_simulation(algorithm, arm_means, time_horizons, strategy["strategy_fn"], rng = rng, **strategy["params"])

    # Save detailed results to CSV (Hier füge den try-except Block ein)
    detailed_results_path = os.path.join(results_dir, f'results_{combination_name}.csv')
    try:
        algorithm.save_results_to_csv(detailed_results_path)
    except Exception as e:
        print(f"Error saving detailed results to {detailed_results_path}: {e}")

    # Calculate and save average results to CSV
    avg_results = algorithm.calculate_average_results()
    avg_results_path = os.path.join(results_dir, f'average_results_{combination_name}.csv')
    save_average_results(avg_results, avg_results_path)


def run_simulation(algorithm, strategy, combinations, time_horizons, seed=global_seed):
    with ProcessPoolExecutor(max_workers=None) as executor_inner:
        futures_inner = [
            executor_inner.submit(run_simulation_inner, algorithm, strategy, arm_means, combination_name, time_horizons, seed)
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

    # Call the Value at Risk calculation
    run_value_at_risk(
    algorithm_strategy_pairs, 
    algorithm_groups, 
    combinations, 
    alpha_values, 
    base_path
    )