# Variance-aware Algorithms for Stochastic Bandit Problems

This repository contains the implementation of various multi-armed bandit algorithms and a dashboard for visualizing their performance. The goal is to compare the effectiveness of different algorithms in maximizing rewards and minimizing regret over time.

## Algorithms and Tuning Parameters

The following algorithms are implemented, each with its own set of tuning parameters:

- **ETC (Explore-then-Commit)**: Explores all available arms for a certain number of rounds before committing to the arm with the highest estimated reward.
   - Tuning Parameters: `exploration_rounds`
   - Scenarios:
      - `exploration_rounds`: 10
      - `exploration_rounds`: 100
      - `exploration_rounds`: 1000
      - `exploration_rounds`: 10000
      - `exploration_rounds`: 100000

- **Epsilon-Greedy**: Balances exploration and exploitation by choosing a random action with probability epsilon and the action with the highest estimated reward with probability \(1 - \epsilon\).
   - Tuning Parameters: `epsilon`
   - Scenarios:
      - `epsilon`: 0.5
      - `epsilon`: 0.1
      - `epsilon`: 0.01
      - `epsilon`: 0.05
      - `epsilon`: 0.005

- **UCB (Upper Confidence Bound)**: Selects the arm with the highest upper confidence bound to balance exploration and exploitation.
   - Tuning Parameters: None

- **UCB-Tuned**: Adjusts the confidence bound by considering the variance of the rewards.
   - Tuning Parameters: None

- **UCB-V**: Incorporates variance estimates into the upper confidence bounds.
   - Tuning Parameters: `theta`, `c`, `b`
   - Scenarios:
      - `theta`: 1, `c`: 1, `b`: 1

- **PAC-UCB**: Guarantees with high probability that the regret is close to the optimal policy.
   - Tuning Parameters: `c`, `b`, `q`, `beta`
   - Scenarios:
      - `c`: 1, `b`: 1, `q`: 1.3, `beta`: 0.05

- **UCB-Improved**: Enhances UCB with more sophisticated exploration strategies.
   - Tuning Parameters: `delta`
   - Scenarios:
      - `delta`: 1

- **EUCBV (Efficient-UCB with Variance)**: Uses empirical estimates of variance to adjust the upper confidence bounds.
   - Tuning Parameters: `rho`
   - Scenarios:
      - `rho`: 0.5


## Bandit Model

The bandit model used in this repository focuses on a multi-armed bandit problem with Bernoulli-distributed arms. The arms are set with the reward probabilities for each arm of $[0.8, 0.89, 0.895, 0.9]$ and can be chosen for two- or three-armed scenarios as well as all possible permutations

Each algorithm is run for 100 rounds, and the results are stored in separate directories for different time steps. Additionally, there is a 'results_average' file for each algorithm, providing the average values for each time step based on 100 samples.

## Plots in the Dashboard

Visualizations and dashboards were created using Plotly and Dash. There is a dashboard available with the following 

1. **Average Total Reward Over Time**: Displays how effectively each algorithm maximizes rewards over time.
2. **Average Regret Over Time**: Shows how well each algorithm minimizes regret over time.
3. **Reward Distribution**: A boxplot showing the distribution of zero and one rewards for each algorithm.
4. **Distribution of Total Regret at Timestep 100,000**: A histogram of total regret values at timestep 1,000,000 across 100 iterations for a selected algorithm.
5. **Value-at-Risk (VaR) Function**: Displays the VaR function for alpha values 0.01, 0.05, and 0.1, indicating the maximum potential loss at a given confidence level.
6. **Proportion of Suboptimal Arms Pulled**: Shows the proportion of suboptimal arm selections compared to all selections up to each timestep.

## Setup Instructions

## 1. Clone the Repository

First, you need to clone the repository from GitHub to your local machine. Open your terminal (or command prompt) and run the following command:

```bash
git clone https://github.com/eelisee/bandit_playground.git
cd bandit_playground
```

## 2. Set Up a Virtual Environment

It is strongly recommended to use a virtual environment to manage the project's dependencies. You can create and activate a virtual environment by running the following commands:

__For macOS/Linux:__

```bash
python3 -m venv .venv
source .venv/bin/activate
```

__For Windows:__
```bash
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install Dependencies

Once the virtual environment is activated, you need to install the required Python packages. Install them by running the following command:

```bash
pip install -r requirements.txt
```

This command will install all the dependencies listed in the ```requirements.txt``` file. Ensure that all packages install without errors.

## 4. Running the Dashboard

Once the installation is complete, you can start the dashboard by running the following command:

```bash
python src/dashboard.py
```

After the command runs, your default web browser should automatically open with the dashboard at this URL:

```bash
http://127.0.0.1:8050
```

If it doesn't open automatically, you can manually copy and paste this URL into your browser.
