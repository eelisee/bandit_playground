import numpy as np
import math

class RAVEN_UCB:
    def __init__(self, alpha0=1.0, beta0=1.0, epsilon=1e-2):
        self.alpha0 = alpha0
        self.beta0 = beta0
        self.epsilon = epsilon
        self.counts = None
        self.means = None
        self.S2 = None

    def initialize(self, num_arms):
        self.counts = np.zeros(num_arms, dtype=int)
        self.means = np.zeros(num_arms, dtype=float)
        self.S2 = np.zeros(num_arms, dtype=float)

    def select_arm(self, t):
        num_arms = len(self.counts)
        # Pull each arm once initially
        for arm in range(num_arms):
            if self.counts[arm] == 0:
                return arm

        # Compute alpha_t
        alpha_t = self.alpha0 / math.log(t + self.epsilon)

        # Compute scores for each arm
        scores = np.zeros(num_arms)
        for k in range(num_arms):
            scores[k] = (
                self.means[k] 
                + alpha_t * math.sqrt(math.log(t + 1) / (self.counts[k] + 1))
                + self.beta0 * math.sqrt(self.S2[k] / (self.counts[k] + 1) + self.epsilon)
            )
        return np.argmax(scores)

    def update(self, chosen_arm, reward):
        n = self.counts[chosen_arm] + 1
        prev_mean = self.means[chosen_arm]
        # Update mean
        self.means[chosen_arm] += (reward - prev_mean) / n
        # Update variance estimator
        if n > 1:
            self.S2[chosen_arm] += (reward - prev_mean) * (reward - self.means[chosen_arm])
            self.S2[chosen_arm] /= (n - 1)
        else:
            self.S2[chosen_arm] = 0.0
        self.counts[chosen_arm] = n


def RAVEN_UCB_simulation(arm_means, num_arms, total_steps, rng=None, **kwargs):
    """
    Simulates the RAVEN-UCB algorithm for Bernoulli bandits.

    Parameters:
    -----------
    arm_means : list or np.array
        True means of each arm.
    num_arms : int
        Number of arms.
    total_steps : int
        Total number of steps to simulate.
    rng : np.random.Generator
        Random number generator.
    alpha0, beta0, epsilon : floats
        Algorithm hyperparameters.

    Returns:
    --------
    dict
        Dictionary with total_rewards, suboptimal_arms, regret, zeros_counts, ones_counts.
    """
    if rng is None:
        rng = np.random.default_rng()

    alpha0 = kwargs.get("alpha0", 1.0)
    beta0 = kwargs.get("beta0", 1.0)
    epsilon = kwargs.get("epsilon", 1e-2)

    raven = RAVEN_UCB(alpha0=alpha0, beta0=beta0, epsilon=epsilon)
    raven.initialize(num_arms)

    total_reward = 0
    suboptimal_arms_count = 0
    total_regret = 0
    zeros_count = 0
    ones_count = 0

    total_rewards = np.zeros(total_steps)
    suboptimal_arms = np.zeros(total_steps, dtype=int)
    regret = np.zeros(total_steps)
    zeros_counts = np.zeros(total_steps, dtype=int)
    ones_counts = np.zeros(total_steps, dtype=int)

    best_arm = np.argmax(arm_means)

    for t in range(1, total_steps + 1):
        arm = raven.select_arm(t)
        reward = rng.binomial(1, arm_means[arm])

        raven.update(arm, reward)

        total_reward += reward
        total_rewards[t - 1] = total_reward

        # Track zeros and ones
        if reward == 0:
            zeros_count += 1
        else:
            ones_count += 1
        zeros_counts[t - 1] = zeros_count
        ones_counts[t - 1] = ones_count

        # Track suboptimal arms and regret
        if arm != best_arm:
            suboptimal_arms_count += 1
            total_regret += arm_means[best_arm] - arm_means[arm]
        suboptimal_arms[t - 1] = suboptimal_arms_count
        regret[t - 1] = total_regret

    return {
        "total_rewards": total_rewards,
        "suboptimal_arms": suboptimal_arms,
        "regret": regret,
        "zeros_counts": zeros_counts,
        "ones_counts": ones_counts
    }