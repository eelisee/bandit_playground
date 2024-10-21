# Instructions to Add a New Algorithm

This document provides step-by-step instructions to add a new algorithm to the repository.

## Step 1: Create a New Branch
1. Open your terminal.
2. Navigate to the repository directory.
3. Create and switch to a new branch:
    ```sh
    git checkout -b add-new-algorithm
    ```

## Step 2: Implement the Algorithm
1. Navigate to the `src/algorithms` directory.
2. Create a new file for your algorithm, e.g., `new_algorithm.py`.
3. Implement your algorithm in the new file. Ensure you follow the repository's coding standards and include necessary comments and documentation.


## Step 2.1: Add Algorithm to the Dashboard
1. Open the `src/dashboard.py` file.
2. Locate the `algorithm_data` dictionary.
3. Add an entry for your new algorithm with the corresponding values. For example:
    ```python
    algorithm_data['new_algorithm'] = {
        'name': 'New Algorithm',
        'description': 'Description of the new algorithm',
        'parameters': {
            'param1': 'Description of param1',
            'param2': 'Description of param2'
        }
    }
    ```
4. Save the changes to `dashboard.py`.


## Step 3: Write Unit Tests
1. Navigate to the `tests` directory.
2. Create a new test file for your algorithm, e.g., `test_new_algorithm.py`.
3. Write unit tests to verify the correctness of your algorithm. Ensure you cover various edge cases.

## Step 4: Update Documentation
1. Navigate to the `docs` directory.
2. Update the relevant documentation files to include information about your new algorithm.
3. Ensure you provide a detailed description, usage examples, and any necessary diagrams or illustrations.

## Step 5: Run Tests
1. Run the test suite to ensure all tests pass:
    ```sh
    pytest
    ```
2. Fix any issues if tests fail.

## Step 6: Commit and Push Changes
1. Add your changes to the staging area:
    ```sh
    git add .
    ```
2. Commit your changes with a descriptive message:
    ```sh
    git commit -m "Add new algorithm and corresponding tests"
    ```
3. Push your changes to the remote repository:
    ```sh
    git push origin add-new-algorithm
    ```

## Step 7: Create a Pull Request
1. Go to the repository on GitHub.
2. Create a new pull request from your branch.
3. Provide a detailed description of your changes and request a review.

## Step 8: Address Review Feedback
1. Address any feedback provided by reviewers.
2. Make necessary changes and push them to your branch.
3. Once approved, merge your pull request.

Congratulations! You have successfully added a new algorithm to the repository.