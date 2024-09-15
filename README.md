# Variance-aware Algorithms for Stochastic Bandit Problems
Exploration-Exploitation Trade-Off of Bandit Algorithms in Comparison

This repository contains the implementation of various multi-armed bandit algorithms and a dashboard for visualizing their performance. The goal is to compare the effectiveness of different algorithms in maximizing rewards and minimizing regret over time. Below is a brief overview of each algorithm's functionality:

- **ETC (Explore-then-Commit)**: Explores all available arms for a certain number of rounds before committing to the arm with the highest estimated reward.
- **Epsilon-Greedy**: Balances exploration and exploitation by choosing a random action with probability epsilon and the action with the highest estimated reward with probability \(1 - \epsilon\).
- **UCB (Upper Confidence Bound)**: Selects the arm with the highest upper confidence bound to balance exploration and exploitation.
- **UCB-Normal**: A variant of UCB designed for normally distributed rewards.
- **UCB-Tuned**: Adjusts the confidence bound by considering the variance of the rewards.
- **UCB-V**: Incorporates variance estimates into the upper confidence bounds.
- **PAC-UCB**: Guarantees with high probability that the regret is close to the optimal policy.
- **UCB-Improved**: Enhances UCB with more sophisticated exploration strategies.
- **EUCBV (Efficient-UCB with Variance)**: Uses empirical estimates of variance to adjust the upper confidence bounds.
- **Not Variance Aware**: A combined result of algorithms that do not consider variance.
- **Variance Aware**: A combined result of algorithms that consider variance.

## Bandit Model

The bandit model used in this repository focuses on a 2-armed bandit problem with Bernoulli-distributed arms for most algorithms and Gaussian-distributed arms for the UCB-Normal algorithm. The arms are set with three different reward scenarios:

1. [0.9, 0.8]
2. [0.9, 0.895]
3. [0.5, 0.495]

For the UCB-Normal algorithm, the corresponding variances are adjusted to match the Bernoulli settings.

Each algorithm is run for 100 rounds, and the results are stored in separate directories for different time steps. Additionally, there is a 'results_average' file for each algorithm, providing the average values for each time step based on 100 samples.

## Plots in the Dashboard

Visualizations and dashboards were created using Plotly and Dash. There is a dashboard available with the following 

1. **Average Total Reward Over Time**: Displays how effectively each algorithm maximizes rewards over time.
2. **Average Regret Over Time**: Shows how well each algorithm minimizes regret over time.
3. **Reward Distribution**: A boxplot showing the distribution of zero and one rewards for each algorithm.
4. **Distribution of Total Regret at Timestep 100,000**: A histogram of total regret values at timestep 100,000 across 100 iterations for a selected algorithm.
5. **Value-at-Risk (VaR) Function**: Displays the VaR function for alpha values 0.01, 0.05, and 0.1, indicating the maximum potential loss at a given confidence level.
6. **Proportion of Suboptimal Arms Pulled**: Shows the proportion of suboptimal arm selections compared to all selections up to each timestep.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/eelisee/varianceinucbalgorithms.git
   cd varianceinucbalgorithms
   
2. **Install Dependencies**

   Ensure you have Python installed. Then, install the required packages using pip:
   ```bash
   pip install -r requirements.txt

4. **Run Algorithms**
   
   Navigate to the 1_algorithms_code directory and run the algorithms to generate results:

   ```bash
   python 1_ETC.py
   python 2_Greedy.py
   ...
   python 9_EUCBV.py

5. You can also calculate the average results and VaR values:

   ```bash
   python calculate_average.py
   python calculate_var.py

6. **Run the Dashboard**

   Navigate to the 3_dashboard directory and start the dashboard:
   
   ```bash
   python dashboard.py

Open your browser and go to http://127.0.0.1:8050 to view the dashboard.
   
For further details on the algorithms, simulation setup, and visualizations, please refer to the corresponding sections in the associated thesis in 0_general.







