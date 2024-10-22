import numpy as np
import math

def UCB_Improved_simulation(arm_means, num_arms, total_steps, **kwargs):
    """
    Simulates the UCB-Improved algorithm over given time horizons.

    Parameters:
    -----------
    algorithm : BanditAlgorithm
        The bandit algorithm instance to store the results.
    arm_means : in
        The arm_means array.
    total_steps : list
        A list of time horizons at which to record the results.

    Returns:
    --------
    dict
        A dictionary where keys are time horizons and values are tuples of (total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count).
    """

    delta = kwargs.get('delta')  # Get delta from kwargs

    num_arms = len(arm_means)  # Number of arms
    rewards = np.zeros(num_arms)  # Rewards for each arm
    pulls = np.zeros(num_arms)  # Number of pulls for each arm
    total_reward = 0  # Total reward accumulated
    suboptimal_arms_count = 0  # Count of suboptimal arms pulled
    total_regret = 0  # Total regret accumulated
    zeros_count = 0  # Count of zero rewards
    ones_count = 0  # Count of one rewards
    
    B = list(range(num_arms))  # List of active arms
    UCB_Improved_max = np.zeros(num_arms)  # UCB values for each arm

    first_phase_end = int(np.floor(0.5 * np.log2(total_steps / np.exp(1))))  # End of the first phase
    
    t = 0  # Phase variable
    z = 0  # Time steps
    
    # Arrays to store results at each time step
    regret = np.zeros(total_steps)
    suboptimal_arms = np.zeros(total_steps, dtype=int)
    total_rewards = np.zeros(total_steps)
    zeros_counts = np.zeros(total_steps, dtype=int)
    ones_counts = np.zeros(total_steps, dtype=int)
    
    while z < total_steps:
        if t < first_phase_end:
            # First phase: Explore all arms
            for m in B:
                max_pulls = math.ceil((2 * np.log(total_steps * delta**2)) / delta**2)
                if pulls[m] <= max_pulls:
                    reward = np.random.binomial(1, arm_means[m])  # Simulate pulling arm m
                    rewards[m] += reward
                    pulls[m] += 1
                    total_reward += reward
                    total_regret += np.max(arm_means) - arm_means[m]
                    if reward == 0:
                        zeros_count += 1
                    else:
                        ones_count += 1
                    if m != np.argmax(arm_means):
                        suboptimal_arms_count += 1
                    z += 1  # Increase the time step after each pull
                    total_rewards[z - 1] = total_reward
                    regret[z - 1] = total_regret
                    suboptimal_arms[z - 1] = suboptimal_arms_count
                    zeros_counts[z - 1] = zeros_count
                    ones_counts[z - 1] = ones_count
                    if z >= total_steps:
                        break
            
            if z < total_steps:  # Only eliminate if time remains
                # Calculate UCB values and eliminate suboptimal arms
                UCB_Improved_max = max((rewards[j] / pulls[j]) - np.sqrt((np.log(total_steps * delta**2)) / (2 * max_pulls)) for j in B)
                B = [k for k in B if (rewards[k] / pulls[k]) + np.sqrt((np.log(total_steps * delta**2)) / (2 * max_pulls)) >= UCB_Improved_max]
                delta /= 2  # Halve delta
                t += 1  # Move to the next phase
        else:
            # Second phase: Exploit the best arm
            if len(B) == 1:
                best_arm = B[0]
            else:
                best_arm = max(B, key=lambda k: rewards[k] / pulls[k])
            reward = np.random.binomial(1, arm_means[best_arm])
            total_reward += reward
            pulls[best_arm] += 1
            total_regret += np.max(arm_means) - arm_means[best_arm]
            if reward == 0:
                zeros_count += 1
            else:
                ones_count += 1
            if best_arm != np.argmax(arm_means):
                suboptimal_arms_count += 1
            z += 1  # Increase the time step after each pull
            total_rewards[z - 1] = total_reward
            regret[z - 1] = total_regret
            suboptimal_arms[z - 1] = suboptimal_arms_count
            zeros_counts[z - 1] = zeros_count
            ones_counts[z - 1] = ones_count

    return {
        "total_rewards": total_rewards,
        "suboptimal_arms": suboptimal_arms,
        "regret": regret,
        "zeros_counts": zeros_counts,
        "ones_counts": ones_counts
    }