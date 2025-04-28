import numpy as np
import os
from config import base_path

def general_simulation(algorithm, arm_means, parameters, strategy_fn, rng =None, **kwargs):
    """
    Runs a general simulation for the specified bandit algorithm over given parameters and arm means using a provided simulation function.

    Parameters:
    -----------
    algorithm : BanditAlgorithm
        The bandit algorithm instance to store the results.
    parameters : list
        A list of parameters (timesteps) for which to record the results.
    arm_means : numpy.ndarray
        The true means of each arm.
    simulation_func : function
        The simulation function to run for the algorithm. This function should accept the same parameters as ETC_simulation and return results in a similar format.

    Returns:
    --------
    None
    """

    max_time_horizon = max(parameters)
    num_arms = len(arm_means)
    
    for iteration in range(1, 101):
        results = strategy_fn(arm_means, num_arms, max_time_horizon, rng=rng, **kwargs)
        
        for param in parameters:
            total_reward = results["total_rewards"][param - 1]
            suboptimal_arms_count = results["suboptimal_arms"][param - 1]
            total_regret = results["regret"][param - 1]
            zeros_count = results["zeros_counts"][param - 1]
            ones_count = results["ones_counts"][param - 1]

            algorithm.add_result(param, iteration, total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count)


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

# Ensure directories are created before saving results
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
