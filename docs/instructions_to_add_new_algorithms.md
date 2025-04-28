# Instructions to add a new Algorithm

## Overview
This document provides step-by-step instructions to add a new algorithm to the repository.

## Instructions

### Step 1: Create a New Branch
1. Open your terminal.
2. Navigate to the repository directory.
3. Create and switch to a new branch:
    ```sh
    git checkout -b add-new-algorithm
    ```

### Step 2: Implement the Algorithm
1. Navigate to the `src/algorithms` directory.
2. Create a new file for your algorithm, e.g., `new_algorithm.py`.
3. Implement your algorithm in the new file. Ensure you follow the repository's coding standards and include necessary comments and documentation:

#### Run Algorithm for Different Scenarios
- **General Imports**: Ensure you include the necessary imports at the beginning of your file:
    ```python
    import numpy as np
    from src.bandit_algorithm import BanditAlgorithm
    ```
- **Algorithm Structure**:  
  Create a subclass of `BanditAlgorithm` and implement the required methods, especially `run(self, arm_distributions, seed)`.

- **Using Configured Combinations**:  
  The different configurations (e.g., arm distributions, order of arms, etc.) are already defined in the central configuration file.  
  Your algorithm will automatically be run across all combinations defined there — no need to manually create or save results for each scenario.

- **Save Results Automatically**:  
  Thanks to the modular structure, your algorithm's results will be saved automatically if you use the `BanditAlgorithm` framework correctly.  
  No manual saving or handling of result files is necessary.

- **Example Orientation**:  
  To simplify your work, you can closely orient yourself to the structure of the `ETC` algorithm (`etc.py`) or any other existing algorithm.

- **Add Algorithm to `src/config.py`**:
  Import your algorithm via 
  ```python
  from algorithms.new_algorithm import class_of_new_algorihm
  ```

  Add your algorithm and its corresponding parameters to the `algorithm_strategy_pairs` and run the `simulation.py`. The resuöts will be saved as `{algorithm.name}_results_{combination}.csv`, `{algorithm.name}_average_results_{combination}.csv` and `/value_at_risk/...` in the corresponding folder  `../data/new_algorithm`

### Step 3: Add Algorithm to the Dashboard
1. Open the `src/dashboard.py` file.
2. Locate the `algorithm_data` dictionary.
3. Add an entry for your new algorithm with the corresponding values. For example:
    ```python
    algorithm_data = { 
        # Existing algorithms ...

        # Add your algorithm to corresponding group
        {"label": "10_youralgorithm", "value": "10_youralgorithm", "color": "#black", "line_style": "dash"},
    }
    ```
4. Save the changes to `dashboard.py`.

### Step 4: Update Documentation
1. Navigate to the `docs` directory.
2. Update the documentation file `documentation.md` to include information about your new algorithm.
3. Ensure you provide a detailed description, usage examples, and any necessary diagrams or illustrations.

### Step 5: Commit and Push Changes
1. Add your changes to the staging area:
    ```sh
    git add .
    ```
2. Commit your changes with a descriptive message:
    ```sh
    git commit -m "Add new algorithm (and corresponding tests)"
    ```
3. Push your changes to the remote repository:
    ```sh
    git push origin add-new-algorithm
    ```

### Step 6: Create a Pull Request
1. Go to the repository on GitHub.
2. Create a new pull request from your branch.
3. Provide a detailed description of your changes and request a review.

### Step 7: Address Review Feedback
1. Address any feedback provided by reviewers.
2. Make necessary changes and push them to your branch.
3. Once approved, merge your pull request.

Congratulations! You have successfully added a new algorithm to the repository.

## Conclusion 

Adding a new algorithm to the repository involves several steps, from creating a new branch to updating documentation and addressing review feedback. By following these instructions, you ensure that your algorithm is well-integrated and maintains the repository's standards. Thank you for your contribution!