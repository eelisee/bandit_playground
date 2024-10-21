# Documentation of the Simulation, Algorithms and Scenarios

## Overview 

This documentation provides an overview of the implemented algorithms, the different simulation scenarios, and the interactive dashboard used for visualization. The repository aims to help students understand and extend the algorithms used in multi-armed bandit problems.

## Simulation

### 1. Implemented Algorithms

Nine multi-armed bandit (MAB) algorithms are implemented in this simulation, each following a distinct approach to balance exploration and exploitation:

**1_ETC** - ETC (Explore-Then-Commit): This algorithm first explores each arm a set number of times before committing to the one with the highest average reward. It draws each arm 100 times during the exploration phase.
  
**2_Greedy** - ε-Greedy: Selects the best-known arm most of the time (exploitation), but with a small probability (ε = 0.05), it selects a random arm to explore. This balances exploitation with exploration over a long time horizon.
  
**3_UCB** - UCB (Upper Confidence Bound): Chooses arms based on upper confidence bounds of expected rewards, factoring in both reward estimates and uncertainty due to limited sampling.
  
**4_UCB-Normal** - UCB-Normal: Uses Gaussian-distributed rewards rather than Bernoulli-distributed ones, making it suitable for normally distributed payoffs. The rewards are drawn with mean values and variances corresponding to the Bernoulli arm settings.
  
**5_UCB-Tuned** - UCB-Tuned: An extension of UCB that adjusts the exploration bonus based on the variance of the rewards.
  
**6_UCB-V** - UCB-V: Utilizes an exploration term based on the variance of rewards. It incorporates three parameters with values chosen to ensure logarithmic regret.
  
**7_PAC-UCB** - PAC-UCB: Adapts UCB-V by using an exploration function independent of time. The parameters for the exploration function are set to facilitate statistically significant results.
  
**8_UCB-Improved** - UCB-Improved: Introduces a mechanism to reduce potentially suboptimal arms over time by halving a tuning parameter and limiting arm draws to one per time step.
  
**9_EUCBV** - Efficient-UCBV: Combines UCB-V and UCB-Improved approaches, adding parameters for arm elimination and exploration regulation.

#### Algorithm Groups

The implemented algorithms can be categorized into three groups based on their awareness of reward variance and their approach to balancing exploration and exploitation:

- **Standard Algorithms**: These are the more traditional approaches to the multi-armed bandit problem, often serving as benchmarks for comparison. The standard algorithms include:
    - **ETC (Explore-Then-Commit)**
    - **ε-Greedy**
    - **UCB (Upper Confidence Bound)**
    - **UCB-Normal**

- **Non-variance-aware Algorithms**: These algorithms do not explicitly consider the variance of rewards but still employ sophisticated strategies to manage exploration and exploitation. The non-variance-aware algorithms include:
    - **PAC-UCB**
    - **UCB-Improved**

- **Variance-aware Algorithms**: These algorithms incorporate the variance of rewards into their decision-making process, allowing for more nuanced exploration strategies. The variance-aware algorithms include:
    - **UCB-Tuned**
    - **UCB-V**
    - **EUCBV**

Categorizing the algorithms in this manner helps in understanding their underlying mechanisms and the scenarios in which they might perform best.


### 2. Simulation Scenarios

The simulations are based on three different cases for a two-armed bandit problem, each with different reward settings to test algorithm performance in various levels of difficulty:

- **ver1** - Easy Case: Rewards are 0.9 for the optimal arm and 0.8 for the suboptimal arm, simulating a clear distinction between arms.
  
- **ver2** - Moderate Case: Rewards are 0.9 and 0.895, making it challenging for algorithms to distinguish between the arms due to the small difference in expected rewards.
  
- **ver3** - Difficult Case: Rewards are set to 0.5 and 0.495, presenting a more difficult scenario where the overall rewards are low, and the arms are nearly identical.

For the UCB-Normal algorithm, rewards follow a Gaussian distribution, with variances corresponding to those derived from the Bernoulli setting.

### 3. Overview of Plots

The dashboard provides six plots to analyze algorithm performance. It is implemented using Plotly Dash, with a user interface allowing parameter adjustments and scenario selection. Below is a description of each plot and the available adjustable parameters:

1. **Average Total Reward Over Time**: Displays how the cumulative reward of each algorithm increases over time, indicating their effectiveness in maximizing rewards.
   
2. **Average Regret Over Time**: Shows the total difference between the optimal and selected rewards over time, highlighting how well each algorithm minimizes regret.
   
3. **Reward Distribution Histogram**: Compares the counts of zero and one rewards for each algorithm, providing insights into the frequency of different reward outcomes.
   
4. **Total Regret Distribution at Time Step 100,000**: Shows the spread of regret values for a selected algorithm, providing insights into variability in performance.
   
5. **Value at Risk (VaR) Function**: Illustrates the potential maximum loss for given α-values (0.01, 0.05, 0.1), offering a measure of risk.
   
6. **Proportion of Suboptimal Arm Pulls Over Time**: Displays the ratio of suboptimal to total pulls, indicating how often suboptimal arms were chosen, thus demonstrating the exploration-exploitation balance.

#### Adjustable Parameters

- **Distribution of Arms**: Choose between different reward distributions for the bandit arms (ver1, ver2, ver3).
- **Order of Arms**: Adjust the order of the optimal and suboptimal arms in the array (Optimal First, Suboptimal First).
- **α for VaR Calculation**: Select the α-value for the VaR plot.
- **Algorithm for Regret Distribution Plot**: Choose which algorithm's regret distribution to display.

The dashboard setup separates these configuration options on the left sidebar, while the right section displays the corresponding visualizations.

## Conclusion

This documentation provides a comprehensive overview of the multi-armed bandit algorithms implemented in this repository, along with detailed descriptions of the simulation scenarios and the interactive dashboard used for visualization. By categorizing the algorithms based on their approach to handling reward variance and balancing exploration and exploitation, users can better understand the strengths and weaknesses of each method. The simulation scenarios offer a range of difficulties to test algorithm performance, while the dashboard's plots and adjustable parameters allow for in-depth analysis and comparison. This resource aims to facilitate learning and experimentation with multi-armed bandit problems, making it a valuable tool for students and researchers alike.