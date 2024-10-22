import numpy as np

def ETC_simulation(arm_means, num_arms, max_time_horizon, **kwargs):
    """
    Simulates the Exploration-Then-Commit (ETC) algorithm over the time horizon.

    Parameters:
    -----------
    arm_means : numpy.ndarray
        The true means of each arm.
    num_arms : int
        The number of arms in the bandit problem.
    max_time_horizon : int
        The maximum number of timesteps to simulate.
    exploration_rounds : int, optional
        The number of rounds to explore each arm before committing to the best (default is 1000).

    Returns:
    --------
    dict
        A dictionary with the total reward, suboptimal arms count, total regret, zeros count, and ones count
        for each timestep up to the max_time_horizon.
    """

    # Get the number of exploration rounds from kwargs, default is None
    exploration_rounds = kwargs.get('exploration_rounds')

    # Initialize arrays to store results
    suboptimal_arms = np.zeros(max_time_horizon, dtype=int)
    regret = np.zeros(max_time_horizon)
    zeros_counts = np.zeros(max_time_horizon, dtype=int)
    ones_counts = np.zeros(max_time_horizon, dtype=int)
    total_rewards = np.zeros(max_time_horizon)
    
    # Initialize counters and accumulators
    total_reward = 0
    zeros_count = 0
    ones_count = 0
    rewards = np.zeros(num_arms)
    counts = np.zeros(num_arms, dtype=int)
    suboptimal_arms_count = 0
    total_regret = 0

    for t in range(1, max_time_horizon+1):
        # Exploration phase: cycle through each arm
        if t <= exploration_rounds * num_arms:
            arm = (t - 1) % num_arms
        else:
            # Exploitation phase: commit to the arm with the highest estimated reward
            arm = np.argmax(rewards / counts)

        # Simulate pulling the arm and getting a reward (1 or 0)
        reward = np.random.binomial(1, arm_means[arm])
        
        # Update counts and rewards for the chosen arm
        counts[arm] += 1
        rewards[arm] += reward
        total_reward += reward
        total_rewards[t - 1] = total_reward

        # Update zero and one counts
        if reward == 0:
            zeros_count += 1
        else:
            ones_count += 1

        zeros_counts[t - 1] = zeros_count
        ones_counts[t - 1] = ones_count

        # Check if the chosen arm is suboptimal
        if arm != np.argmax(arm_means):
            suboptimal_arms_count += 1
            total_regret += np.max(arm_means) - arm_means[arm]

        # Update regret and suboptimal arms count
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