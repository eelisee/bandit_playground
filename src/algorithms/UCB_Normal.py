import numpy as np
import math

def UCB_Normal_simulation(arm_means, num_arms, total_steps, **kwargs):
    """
    Simulates the UCB algorithm over given time horizons.

    Parameters:
    -----------
    arm_means : list
        The means of each arm.
    num_arms : int
        The number of arms.
    total_steps : int
        The total number of steps in the simulation.
    kwargs : dict
        Additional keyword arguments (should include arm_variances).

    Returns:
    --------
    dict
        A dictionary containing total rewards, suboptimal arms, regret, zeros counts, and ones counts.
    """

    # Fetch arm variances from kwargs, default to zeros if not provided
    arm_variances = kwargs.get('arm_variances', np.zeros(num_arms))

    # Initialize variables to track rewards, counts, and other metrics
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
        # Initial exploration phase: ensure each arm is pulled at least a certain number of times
        if any(counts < math.ceil(8 * np.log(total_steps))):
            arm = np.argmin(counts)
        else:
            # Calculate UCB values for each arm
            ucb_values = np.zeros(num_arms)
            for j in range(num_arms):
                if counts[j] > 1:
                    mean_reward = rewards[j] / counts[j]
                    variance = (sum_of_squares[j] - counts[j] * (mean_reward ** 2)) / (counts[j])
                    ucb_values[j] = mean_reward + np.sqrt(16 * variance * np.log(t - 1) / counts[j])
            # Select the arm with the highest UCB value
            arm = np.argmax(ucb_values)
        
        # Sample reward from the normal distribution using arm means and variances
        reward = np.random.normal(arm_means[arm], np.sqrt(arm_variances[arm]))
        counts[arm] += 1
        rewards[arm] += reward
        sum_of_squares[arm] += reward ** 2
        total_reward += reward
        total_rewards[t - 1] = total_reward

        # Track the number of times the reward is less than or equal to the arm mean
        if reward <= arm_means[arm]:
            zeros_count += 1
        else:
            ones_count += 1

        zeros_counts[t - 1] = zeros_count
        ones_counts[t - 1] = ones_count

        # Track suboptimal arm selections and calculate regret
        if arm != np.argmax(arm_means):
            suboptimal_arms_count += 1
            total_regret += np.max(arm_means) - arm_means[arm]

        regret[t - 1] = total_regret
        suboptimal_arms[t - 1] = suboptimal_arms_count

    # Return the results as a dictionary
    return {
        "total_rewards": total_rewards,
        "suboptimal_arms": suboptimal_arms,
        "regret": regret,
        "zeros_counts": zeros_counts,
        "ones_counts": ones_counts
    }