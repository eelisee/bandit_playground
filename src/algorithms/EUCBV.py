import numpy as np
import math

def EUCBV_simulation(arm_means, num_arms, total_steps, **kwargs):
    """
    Simulates the epsilon-greedy algorithm over given time horizons.

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

    # Extract rho parameter from kwargs
    rho = kwargs.get("rho")
    K = len(arm_means)  # Number of arms
    psi = total_steps / (K**2)  # Scaling factor for the algorithm
    
    # Initialize tracking variables
    T_k = np.zeros(K)  # Number of times each arm has been played
    X_k = np.zeros(K)  # Sum of rewards for each arm
    sum_of_squares = np.zeros(K)  # Sum of squared differences for each arm
    
    zeros_count = 0
    ones_count = 0
    
    B_t = set(range(K))  # Set of active arms
    delta_t = 1  # Initial delta value
    total_reward = 0
    suboptimal_arms_count = 0
    total_regret = 0
    
    # Arrays to store results at each time step
    regret = np.zeros(total_steps)
    suboptimal_arms = np.zeros(total_steps, dtype=int)
    total_rewards = np.zeros(total_steps)
    zeros_counts = np.zeros(total_steps, dtype=int)
    ones_counts = np.zeros(total_steps, dtype=int)

    def play_arm(arm, t):
        nonlocal zeros_count, ones_count, total_reward, suboptimal_arms_count, total_regret
        reward = np.random.binomial(1, arm_means[arm])  # Simulate reward
        T_k[arm] += 1
        X_k[arm] += reward
        sum_of_squares[arm] += reward**2
        total_reward += reward
        
        if reward == 0:
            zeros_count += 1
        else:
            ones_count += 1
        
        if arm != np.argmax(arm_means):
            suboptimal_arms_count += 1
            total_regret += np.max(arm_means) - arm_means[arm]

        # Store results at time t
        total_rewards[t] = total_reward
        regret[t] = total_regret
        suboptimal_arms[t] = suboptimal_arms_count
        zeros_counts[t] = zeros_count
        ones_counts[t] = ones_count
        
        return reward

    # Initial play of each arm once
    for arm in range(K):
        play_arm(arm, arm)
    
    M = int(math.floor(0.5 * math.log2(total_steps / math.exp(1))))  # Maximum number of phases
    m = 0  # Current phase
    n_0 = int(math.ceil(math.log(psi * total_steps * delta_t**2) / (2 * delta_t)))  # Initial number of plays per arm
    N_0 = K * n_0  # Total initial plays
    
    for t in range(K, total_steps):
        if len(B_t) == 1:
            # If only one arm is left, play it
            best_arm = next(iter(B_t))
            play_arm(best_arm, t)
            continue
        
        # Select arm with the highest upper confidence bound
        selected_arm = max(B_t, key=lambda arm_index: (X_k[arm_index] / T_k[arm_index]) + math.sqrt((rho * ((sum_of_squares[arm_index] / T_k[arm_index]) - (X_k[arm_index] / T_k[arm_index])**2 + 2) * math.log(psi * total_steps * delta_t)) / (4 * T_k[arm_index])))
        play_arm(selected_arm, t)
        
        # Update the set of active arms
        for arm_index in list(B_t):
            mean_estimate = X_k[arm_index] / T_k[arm_index]
            variance_estimate = (sum_of_squares[arm_index] - T_k[arm_index] * (mean_estimate ** 2)) / T_k[arm_index]
            bound = math.sqrt((rho * (variance_estimate + 2) * math.log(psi * total_steps * delta_t)) / (4 * T_k[arm_index]))
            
            for k in range(K):
                mean_reward = X_k[k] / T_k[k]
                EUCBV = mean_reward - math.sqrt((rho * ((sum_of_squares[k] / T_k[k]) - (X_k[k] / T_k[k])**2 + 2) * math.log(psi * total_steps * delta_t)) / (4 * T_k[k]))
            maximum = np.max(EUCBV)

            if mean_estimate + bound < maximum:
                B_t.remove(arm_index)
        
        # Update delta and n_0 at the end of each phase
        if t >= N_0 and m <= M:
            delta_t /= 2
            B_t = B_t
            n_0 = int(math.ceil(math.log(psi * total_steps * delta_t**2) / (2 * delta_t)))
            N_0 = t + len(B_t) * n_0
            m += 1

    return {
        "total_rewards": total_rewards,
        "suboptimal_arms": suboptimal_arms,
        "regret": regret,
        "zeros_counts": zeros_counts,
        "ones_counts": ones_counts
    }