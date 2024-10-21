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

#### Step 2.2: Run Algorithm for Different Scenarios
1. Ensure your algorithm is run in the standard scenarios: `opt`, `subopt` in combination with versions `1`, `2`, `3` for different arm distributions as described and others listed in in `documentation.md`
3. Define the combinations:
    ```python
    combinations = [
        "opt_ver1", "opt_ver2", "opt_ver3",
        "subopt_ver1", "subopt_ver2", "subopt_ver3"
    ]
    ```
4. Run your algorithm for each combination and save the results as `{algorithm.name}_results_{combination}.csv` in `../data/algorithms_results`
5. Calculate the average results and save them as `{algorithm.name}_average_results_{combination}.csv` in `../data/algorithms_results`

#### Step 2.3: Run Calculations for Dashboard
1. Navigate to the `../src/calculations_for_dashboard/calculate_averages.ipynb` file.
2. Add your new algorithm to the corresponding group and rerun the notebook to update the averages.
3. Navigate to the `../src/calculations_for_dashboard/value_at_risk.ipynb` file.
4. Add your new algorithm to the corresponding group and rerun the notebook to create the data visualized in plot 5.


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


### (Additional) Step 4: Write Unit Tests
1. Navigate to the `tests` directory.
2. Create a new test file for your algorithm, e.g., `test_new_algorithm.py`.
3. Write unit tests to verify the correctness of your algorithm. Ensure you cover various edge cases.

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