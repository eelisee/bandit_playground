import os
from utils.combination import generate_combinations
from utils.bandit_algorithm import BanditAlgorithm

# ====== Algorithm Strategy Pairs ======

# Import simulation functions for each algorithm
from algorithms.ETC import ETC_simulation
from algorithms.Greedy import Greedy_simulation
from algorithms.UCB import UCB_simulation
from algorithms.UCB_Tuned import UCB_Tuned_simulation
from algorithms.UCB_V import UCB_V_simulation
from algorithms.PAC_UCB import PAC_UCB_simulation
from algorithms.UCB_Improved import UCB_Improved_simulation
from algorithms.EUCBV import EUCBV_simulation

# List of algorithms and their corresponding strategies
algorithm_strategy_pairs = [
    (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 10}}),
    (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 100}}),
    (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 1000}}),
    (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 10000}}),
    (BanditAlgorithm("ETC"), {"strategy_fn": ETC_simulation, "params": {"exploration_rounds": 100000}}),
    (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.005}}),
    (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.01}}),
    (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.05}}),
    (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.1}}),
    (BanditAlgorithm("Greedy"), {"strategy_fn": Greedy_simulation, "params": {"epsilon": 0.5}}),
    (BanditAlgorithm("UCB"), {"strategy_fn": UCB_simulation, "params": {}}),
    (BanditAlgorithm("UCB-Tuned"), {"strategy_fn": UCB_Tuned_simulation, "params": {}}),
    (BanditAlgorithm("UCB-V"), {"strategy_fn": UCB_V_simulation, "params": {"theta": 1, "c": 1, "b": 1}}),
    (BanditAlgorithm("PAC-UCB"), {"strategy_fn": PAC_UCB_simulation, "params": {"c": 1, "b": 1, "q": 1.3, "beta": 0.05}}),
    (BanditAlgorithm("UCB-Improved"), {"strategy_fn": UCB_Improved_simulation, "params": { "delta": 1}}),
    (BanditAlgorithm("EUCBV"), {"strategy_fn": EUCBV_simulation, "params": {"rho": 0.5}})
]

# Algorithm group definitions, add algorithms to the respective groups here
algorithm_groups = {
    "Variance-aware UCB Variations": ["UCB-Tuned", "UCB-V", "EUCBV"],
    "Not-variance-aware UCB Variations": ["PAC-UCB", "UCB-Improved"],
    "Standard Algorithms": ["ETC", "Greedy", "UCB"]
}


# ======= Parameters =======

# Define the time horizons for the simulation
time_horizons = [2, 3, 100, 200, 2000, 10000, 20000, 40000, 60000, 80000, 100000, 200000, 400000, 600000, 800000, 1000000]

# Define the possible individual arm values
individual_arm_distribution = [0.9, 0.895, 0.89, 0.85, 0.8]

# Define alpha values
alpha_values = [0.01, 0.05, 0.1]

# Degine the seed for reproducibility in each algorithms simulation
global_seed = 42

# ======= Directory Setup ======

# Generate the combinations
combinations = generate_combinations(individual_arm_distribution)

# Base paths
base_path = os.path.join(os.getcwd(), 'data')