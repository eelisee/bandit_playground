import numpy as np

def UCB_Tuned_simulation(arm_means, num_arms, total_steps):
    """
    Simulates the UCB-Tuned algorithm over given time horizons.

    Parameters:
    -----------
    arm_means : list
        The mean rewards of each arm.
    num_arms : int
        The number of arms.
    total_steps : int
        The total number of steps to simulate.

    Returns:
    --------
    dict
        A dictionary where keys are time horizons and values are tuples of (total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count).
    """

    # Initialize variables
    num_arms = len(arm_means)
    rewards = np.zeros(num_arms)  # Total rewards for each arm
    counts = np.zeros(num_arms)  # Number of times each arm is pulled
    sum_of_squares = np.zeros(num_arms)  # Sum of squares of rewards for each arm
    total_reward = 0  # Total reward accumulated
    suboptimal_arms_count = 0  # Count of suboptimal arm pulls
    total_regret = 0  # Total regret accumulated
    zeros_count = 0  # Count of zero rewards
    ones_count = 0  # Count of one rewards
    regret = np.zeros(total_steps)  # Regret at each step
    suboptimal_arms = np.zeros(total_steps, dtype=int)  # Suboptimal arm pulls at each step
    total_rewards = np.zeros(total_steps)  # Total rewards at each step
    zeros_counts = np.zeros(total_steps, dtype=int)  # Zero rewards count at each step
    ones_counts = np.zeros(total_steps, dtype=int)  # One rewards count at each step

    # Simulation loop
    for t in range(1, total_steps + 1):
        if any(counts == 0):
            # If any arm hasn't been pulled yet, pull the least pulled arm
            arm = np.argmin(counts)
        else:
            # Calculate UCB values for each arm
            UCB = np.zeros(num_arms)
            for k in range(num_arms):
                if counts[k] > 0:
                    mean_reward = rewards[k] / counts[k]
                    variance = (sum_of_squares[k] / counts[k]) - (mean_reward ** 2)
                    V_ks = variance + np.sqrt(2 * np.log(t) / counts[k])
                    exploration_term = np.sqrt((np.log(t) / counts[k]) * min(1 / 4, V_ks))
                    UCB[k] = mean_reward + exploration_term
            # Select the arm with the highest UCB value
            arm = np.argmax(UCB)
        
        # Simulate pulling the arm
        reward = np.random.binomial(1, arm_means[arm])
        counts[arm] += 1
        rewards[arm] += reward
        sum_of_squares[arm] += reward ** 2
        total_reward += reward
        total_rewards[t - 1] = total_reward

        # Update zero and one counts
        if reward == 0:
            zeros_count += 1
        else:
            ones_count += 1

        zeros_counts[t - 1] = zeros_count
        ones_counts[t - 1] = ones_count

        # Update suboptimal arm count and total regret
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
