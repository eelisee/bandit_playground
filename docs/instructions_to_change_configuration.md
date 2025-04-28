# Instructions to Change the Configuration

## Overview
This document provides detailed instructions on how to modify the configuration settings for the simulation environment.  
The configuration is primarily controlled via a central configuration file, ensuring modularity, flexibility, and easy adaptability for new experiments.

## Instructions

### Step 1: Understand the Configuration Structure
The configuration file (`src/config.py`) consists of the following main components:

---

#### 1. Algorithm Strategy Pairs
- **Purpose**: Define which algorithms are available and with which parameters they are run.
- **Structure**: A list of tuples, each containing:
  - A `BanditAlgorithm` instance (the name of the algorithm),
  - A dictionary specifying:
    - The corresponding simulation function (`strategy_fn`),
    - Parameters (`params`) for the algorithm.

- **Adding a New Algorithm**:
  - Import your algorithm's simulation function at the beginning of the config file.
    ```python
    from algorithms.NewAlgorithm import NewAlgorithm_simulation
    ```
  - Add your new algorithm to `algorithm_strategy_pairs`:
    ```python
    (BanditAlgorithm("New-Algorithm"), {"strategy_fn": NewAlgorithm_simulation, "params": {"param1": 10, "param2": 5}})
    ```

- **Important**:  
  Ensure the name provided in `BanditAlgorithm("New-Algorithm")` matches exactly the naming convention used in your dashboard and results files.

---

#### 2. Algorithm Groups
- **Purpose**: Categorize algorithms into logical groups for the dashboard and analysis plots.
- **Structure**: A dictionary where each key is a group name and the value is a list of algorithm names.
  
- **Adding a New Algorithm to a Group**:
  - Insert your new algorithm into an appropriate group, e.g.:
    ```python
    "Standard Algorithms": ["ETC", "Greedy", "UCB", "New-Algorithm"]
    ```
  - Alternatively, create a new group if needed.

---

### Step 2: Adjust Simulation Parameters
The following parameters control the general setup of the simulations:


#### 1. Time Horizons
- **Purpose**: Define the number of steps for which the bandit algorithms are run.
- **Variable**: `time_horizons`
- **Modification**:  
  You can add or remove time horizons from the list as needed:
  ```python
  time_horizons = [1000, 10000, 50000, 100000]  # Example
  ```


#### 2. Individual Arm Distributions
- **Purpose**: Define the expected reward probabilities for each arm (action).
- **Variable**: `individual_arm_distribution`
- **Modification**: Add or adjust the list to reflect different difficulty levels:
```python
individual_arm_distribution = [0.9, 0.8, 0.7]  # Example
```

Note: After modifying this list, the combinations are automatically regenerated via:
```python
combinations = generate_combinations(individual_arm_distribution)
```

#### 3. Alpha Values
- **Purpose**: Used for algorithms that rely on confidence bounds or significance levels (e.g., PAC-UCB).
- **Variable**: `alpha_values`
- **Modification**: Adjust the list based on the precision or strictness you require:
```python
alpha_values = [0.01, 0.05, 0.1]
```

#### 4. Global Seed
- **Purpose**: Ensure reproducibility across simulations.
- **Variable**: `global_seed`
- **Modification**: Set a different integer value if you want to change the randomization:
```python
global_seed = 123
```

Important: Keeping a fixed seed is recommended for experimental reproducibility.

---

### Step 3: Save and Validate Changes
1.	After making changes, save the `config.py` file.
2.	Run a short test simulation to ensure the new configuration is correctly loaded and there are no import or logic errors.
3.	Check that all paths and combinations are generated as expected under the `.../data` folder.