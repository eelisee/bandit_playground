# import numpy as np
# import csv
# import math
# import os

class BanditAlgorithm:
    """
    A class to represent a bandit algorithm and manage its results.

    Attributes:
    -----------
    name : str
        The name of the bandit algorithm.
    results : list
        A list to store results of the algorithm's performance over iterations.
    """

    def __init__(self, name):
        self.name = name
        self.results = []

    def add_result(self, param, iteration, total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count):
        self.results.append([param, iteration, total_reward, suboptimal_arms_count, round(total_regret, 2), zeros_count, ones_count])

    def save_results_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestep', 'Iteration', 'Total Reward', 'Suboptimal Arms', 'Total Regret', 'Zeros Count', 'Ones Count'])
            for result in self.results:
                writer.writerow(result)

    def calculate_average_results(self):
        avg_results = {}
        for result in self.results:
            param = result[0]
            if param not in avg_results:
                avg_results[param] = [0, 0, 0, 0, 0]
            avg_results[param][0] += result[2]  # Total Reward
            avg_results[param][1] += result[3]  # Suboptimal Arms Count
            avg_results[param][2] += result[4]  # Total Regret
            avg_results[param][3] += result[5]  # Zeros Count
            avg_results[param][4] += result[6]  # Ones Count
        
        for param in avg_results:
            avg_results[param] = [param] + [x / 100 for x in avg_results[param]]
        return list(avg_results.values())

def UCB_Tuned_simulation(arm_means, total_steps):
    """
    Simulates the epsilon-greedy algorithm over given time horizons.

    Parameters:
    -----------
    algorithm : BanditAlgorithm
        The bandit algorithm instance to store the results.
    arm_means : in
        The length of the arm_means array.
    total_steps : list
        A list of time horizons at which to record the results.


    Returns:
    --------
    dict
        A dictionary where keys are time horizons and values are tuples of (total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count).
    """

    num_arms = len(arm_means)
    rewards = np.zeros(num_arms)
    counts = np.zeros(num_arms)
    sum_of_squares = np.zeros(num_arms)
    total_reward = 0
    suboptimal_arms_count = 0
    total_regret = 0
    zeros_count = 0
    ones_count = 0
    regret = np.zeros(total_steps)
    suboptimal_arms = np.zeros(total_steps, dtype=int)
    total_rewards = np.zeros(total_steps)
    zeros_counts = np.zeros(total_steps, dtype=int)
    ones_counts = np.zeros(total_steps, dtype=int)

    for t in range(1, total_steps + 1):
        if any(counts == 0):
            arm = np.argmin(counts)
        else:
            UCB = np.zeros(num_arms)
            for k in range(num_arms):
                if counts[k] > 0:
                    mean_reward = rewards[k] / counts[k]
                    variance = (sum_of_squares[k] / counts[k]) - (mean_reward ** 2)
                    V_ks = variance + np.sqrt(2 * np.log(t) / counts[k])
                    exploration_term = np.sqrt((np.log(t) / counts[k]) * min(1 / 4, V_ks))
                    UCB[k] = mean_reward + exploration_term
            arm = np.argmax(UCB)
        
        reward = np.random.binomial(1, arm_means[arm])
        counts[arm] += 1
        rewards[arm] += reward
        sum_of_squares[arm] += reward ** 2
        total_reward += reward
        total_rewards[t - 1] = total_reward

        if reward == 0:
            zeros_count += 1
        else:
            ones_count += 1

        zeros_counts[t - 1] = zeros_count
        ones_counts[t - 1] = ones_count

        if arm != np.argmax(arm_means):
            suboptimal_arms_count += 1
            total_regret += np.max(arm_means) - arm_means[arm]

        regret[t - 1] = total_regret
        suboptimal_arms[t - 1] = suboptimal_arms_count

    return {
        "total_rewards": total_rewards,
        "suboptimal_arms": suboptimal_arms,
        "regret": regret,
        "zeros_counts": zeros_counts,
        "ones_counts": ones_counts
    }

def general_simulation(algorithm, arm_means, parameters, strategy_fn):
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
        results = strategy_fn(arm_means, max_time_horizon)

        for param in parameters:
            total_reward = results["total_rewards"][param - 1]
            suboptimal_arms_count = results["suboptimal_arms"][param - 1]
            total_regret = results["regret"][param - 1]
            zeros_count = results["zeros_counts"][param - 1]
            ones_count = results["ones_counts"][param - 1]

            algorithm.add_result(param, iteration, total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count)


time_horizons = [2, 3, 100, 200, 2000, 10000, 20000, 40000, 60000, 80000, 100000]


algorithms = [
    BanditAlgorithm("5_UCB-Tuned"),
]


arm_means = np.array([0.495, 0.5])

# Basis path
results_path = os.path.join(os.getcwd(), "data", "algorithms_results")

# Perform simulation and save results
for algorithm in algorithms:
    general_simulation(algorithm, arm_means, time_horizons, UCB_Tuned_simulation)
    algorithm.save_results_to_csv(f'{results_path}\{algorithm.name}_results_subopt_ver3.csv')
    avg_results = algorithm.calculate_average_results()
    with open(f'{results_path}\{algorithm.name}_average_results_subopt_ver3.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestep', 'Average Total Reward', 'Average Suboptimal Arms', 'Average Regret', 'Average Zeros Count', 'Average Ones Count'])
        for result in avg_results:
            writer.writerow(result)


