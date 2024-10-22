import numpy as np

def UCB_V_simulation(arm_means, num_arms, total_steps, **kwargs):
    """
    Simulates the UCB-V algorithm over given time horizons.

    Parameters:
    -----------
    algorithm : BanditAlgorithm
        The bandit algorithm instance to store the results.
    arm_means : in
        The length of the arm_means array.
    total_steps : list
        A list of time horizons at which to record the results.
    theta : float
        A parameter for the choice of theta.
    c : float
        A parameter for the choice of c.
    b : float
        A parameter for the choice of b.

    Returns:
    --------
    dict
        A dictionary where keys are time horizons and values are tuples of (total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count).
    """
    # Extract parameters from kwargs
    theta = kwargs.get('theta') 
    c = kwargs.get('c')
    b = kwargs.get('b')

    # Initialize variables
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

    # Main loop over time steps
    for t in range(1, total_steps + 1):
        # Select an arm to pull
        if any(counts < 1):
            # If any arm hasn't been pulled yet, pull the least pulled arm
            arm = np.argmin(counts)
        else:
            # Calculate the UCB-V value for each arm
            B = np.zeros(num_arms)
            for k in range(num_arms):
                if counts[k] > 0:
                    mean_reward = rewards[k] / counts[k]
                    variance = (sum_of_squares[k] - counts[k] * (mean_reward ** 2)) / counts[k]
                    exploration = theta * np.log(t)
                    B[k] = mean_reward + np.sqrt((2 * variance * exploration) / counts[k]) + c * (3 * b * exploration / counts[k])
            # Select the arm with the highest UCB-V value
            arm = np.argmax(B)
        
        # Simulate pulling the arm and receiving a reward
        reward = np.random.binomial(1, arm_means[arm])
        counts[arm] += 1
        rewards[arm] += reward
        sum_of_squares[arm] += reward ** 2
        total_reward += reward
        total_rewards[t - 1] = total_reward

        # Update counts of zeros and ones
        if reward == 0:
            zeros_count += 1
        else:
            ones_count += 1

        zeros_counts[t - 1] = zeros_count
        ones_counts[t - 1] = ones_count

        # Update regret and suboptimal arm counts
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