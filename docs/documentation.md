# Documentation of the Simulation, Algorithms, and Scenarios

## Overview

This documentation provides an overview of the implemented algorithms, the simulation framework, and the interactive dashboard used for analysis. The repository aims to support the study and extension of algorithms for multi-armed bandit problems.

## Simulation

### Implemented Algorithms

The simulation includes eight different multi-armed bandit (MAB) algorithms, each implementing distinct strategies for balancing exploration and exploitation:

- **ETC (Explore-Then-Commit)**: Initially explores each arm a fixed number of times before committing to the arm with the highest observed average reward.
  
- **ε-Greedy**: Selects the arm with the highest estimated reward most of the time, but occasionally explores random arms with probability ε = 0.05.
  
- **UCB (Upper Confidence Bound)**: Selects arms based on upper confidence bounds for the expected reward, balancing exploration and exploitation dynamically.
  
- **UCB-Tuned**: An enhanced version of UCB that adjusts the exploration term based on the observed variance of rewards.
  
- **UCB-V**: Incorporates the empirical variance of rewards into the exploration bonus, improving adaptability to reward variability.
  
- **PAC-UCB**: A variant of UCB-V with an exploration term independent of time, aimed at achieving statistically sound guarantees.
  
- **UCB-Improved**: Implements an elimination strategy, progressively excluding arms based on observed performance while adjusting exploration intensity.
  
- **EUCBV (Efficient-UCBV)**: Combines the principles of UCB-V and UCB-Improved by introducing additional parameters for fine-grained control of exploration and arm elimination.

#### Algorithm Categories

The algorithms can be categorized according to their treatment of reward variance and exploration strategies:

- **Standard Algorithms**:
  - ETC (Explore-Then-Commit)
  - ε-Greedy
  - UCB (Upper Confidence Bound)

- **Non-variance-aware Algorithms**:
  - PAC-UCB
  - UCB-Improved

- **Variance-aware Algorithms**:
  - UCB-Tuned
  - UCB-V
  - EUCBV

This categorization helps to understand the underlying strategies and the contexts in which specific algorithms may perform better.

### Simulation Scenarios

The simulation framework systematically explores all possible combinations of arm reward distributions, instead of relying on a few predefined cases. 

Each simulation run is configured via **Individual Arm Distributions**, specifying the expected reward for each arm individually. This allows for:

- Testing scenarios with clearly distinguishable arms,
- Exploring challenging scenarios with almost identical rewards,
- Assessing performance across a wide range of difficulties.

By considering all combinations within a defined range of arm rewards, the simulation captures a broad spectrum of problem instances, ensuring a comprehensive evaluation of algorithm behavior.

In addition, it is possible to select specific combinations that are more difficult for algorithms to distinguish, facilitating focused experiments on scenarios that stress exploration capabilities.

### Overview of the Dashboard

The interactive dashboard, implemented with Plotly Dash, enables dynamic visualization and comparison of algorithm performance. The dashboard provides the following key plots:

1. **Average Total Reward Over Time**: Displays how the cumulative reward evolves for each algorithm.
   
2. **Average Regret Over Time**: Shows the cumulative difference between the maximum possible and achieved rewards, quantifying the efficiency of learning.
   
3. **Reward Distribution Histogram**: Visualizes the frequency of different rewards (e.g., zeros and ones) achieved by each algorithm.
   
4. **Total Regret Distribution at a Fixed Time Step**: Presents the variability of regret values across simulation runs for a selected algorithm.
   
5. **Value at Risk (VaR) Plot**: Analyzes the risk of extreme losses, plotting VaR for selected significance levels (α-values).
   
6. **Proportion of Suboptimal Arm Pulls Over Time**: Tracks how frequently each algorithm chooses a suboptimal arm, revealing exploration behavior.

#### Adjustable Parameters

The dashboard allows users to configure:

- **Individual Arm Distributions**: Selection of reward probabilities for each arm.
- **Order of Arms**: Define whether the optimal or suboptimal arm is listed first.
- **α-Value for VaR Plot**: Choose the risk threshold (e.g., 0.01, 0.05, 0.1) for Value at Risk calculations.
- **Algorithm for Regret Distribution**: Select the algorithm to analyze in detailed regret distribution plots.

The left sidebar contains the configuration options, while the main area displays the corresponding visualizations.

## Conclusion

This documentation provides a comprehensive description of the algorithms, simulation setup, and dashboard tools available in the repository. By systematically evaluating all combinations of arm distributions and categorizing algorithms based on their strategies, the framework enables thorough analysis and comparison. This resource is intended to support both educational purposes and further research on multi-armed bandit algorithms.