import numpy as np
import math

class UCB1:
    def __init__(self):
        # Initialize counts and values for each arm
        self.counts = []
        self.values = []

    def initialize(self, n_arms):
        # Set counts and values to zero for each arm
        self.counts = [0] * n_arms
        self.values = [0.0] * n_arms

    def select_arm(self):
        n_arms = len(self.counts)
        # Select an arm that has not been tried yet
        for arm in range(n_arms):
            if self.counts[arm] == 0:
                return arm

        total_counts = sum(self.counts)
        ucb_values = [0.0] * n_arms

        # Calculate UCB value for each arm
        for arm in range(n_arms):
            bonus = math.sqrt((2 * math.log(total_counts)) / self.counts[arm])
            ucb_values[arm] = self.values[arm] + bonus

        # Return the arm with the highest UCB value
        return ucb_values.index(max(ucb_values))

    def update(self, chosen_arm, reward):
        # Update counts and values for the chosen arm
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]
        value = self.values[chosen_arm]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[chosen_arm] = new_value


def UCB_simulation(arm_means, num_arms, total_steps):
    """
    Simulates the UCB algorithm over given time horizons.

    Parameters:
    -----------
    arm_means : numpy.ndarray
        The true means of each arm.
    num_arms : int
        The number of arms (length of arm_means array).
    total_steps : int
        The total number of steps to simulate.

    Returns:
    --------
    dict
        A dictionary where keys are time horizons and values are arrays of rewards, suboptimal arms count, total regret, zeros count, and ones count.
    """
    ucb = UCB1()
    ucb.initialize(num_arms)
    
    # Initialize tracking variables
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

    # Run the simulation for the given number of steps
    for t in range(1, total_steps + 1):
        # Select an arm using UCB1 algorithm
        chosen_arm = ucb.select_arm()
        # Simulate the reward for the chosen arm
        reward = np.random.binomial(1, arm_means[chosen_arm])
        counts[chosen_arm] += 1
        ucb.update(chosen_arm, reward)
        rewards[chosen_arm] += reward
        total_reward += reward
        total_rewards[t - 1] = total_reward

        # Track the number of zeros and ones
        if reward == 0:
            zeros_count += 1
        else:
            ones_count += 1

        zeros_counts[t - 1] = zeros_count
        ones_counts[t - 1] = ones_count

        # Track suboptimal arm selections and regret
        if chosen_arm != np.argmax(arm_means):
            suboptimal_arms_count += 1
            total_regret += np.max(arm_means) - arm_means[chosen_arm]

        regret[t - 1] = total_regret
        suboptimal_arms[t - 1] = suboptimal_arms_count

    # Return the results of the simulation
    return {
        "total_rewards": total_rewards,
        "suboptimal_arms": suboptimal_arms,
        "regret": regret,
        "zeros_counts": zeros_counts,
        "ones_counts": ones_counts
    }