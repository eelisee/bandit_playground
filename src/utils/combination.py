from itertools import permutations, combinations, combinations_with_replacement

# Function to generate the unique arm combinations
def generate_combinations(individual_arm_distribution):
    """
    Generate unique combinations of arms from the given distribution.
    This function generates two types of combinations:
    1. Two-arm combinations without repeated arms.
    2. Three-arm combinations allowing at most two repeated arms.
    For each combination, all unique permutations are generated and stored in a set to ensure uniqueness.
    Each permutation is converted to a string representation where each arm value is scaled and concatenated with an underscore.
    Args:
        individual_arm_distribution (list): A list of arm values from which combinations are generated.
    Returns:
        list: A list of tuples where each tuple contains a permutation of arms and its corresponding string representation.
    Raises:
        ValueError: If any value in individual_arm_distribution is greater than 1.
    """

    # Check for values greater than 1
    if any(value > 1 for value in individual_arm_distribution):
        raise ValueError("All values in individual_arm_distribution must be less than or equal to 1.")

    combinations_set = set()  # Using a set to store unique combinations

    # 1. Generate two-arm combinations (no repeated arms)
    two_arm_combinations = combinations(individual_arm_distribution, 2)
    
    for comb in two_arm_combinations:
        # Generate all permutations (unique order) of two-arm combinations
        for perm in permutations(comb):
            combination_name = "_".join(str(int(a * 1000)) for a in perm)
            combinations_set.add((perm, combination_name))

    # 2. Generate three-arm combinations (allow two repeated arms)
    three_arm_combinations = combinations_with_replacement(individual_arm_distribution, 3)
    
    for comb in three_arm_combinations:
        # Ensure that not all arms are the same
        if len(set(comb)) < 3:  # Allow combinations with at most 2 identical arms
            # Generate all permutations (unique order) of three-arm combinations
            for perm in permutations(comb):
                # Check to ensure not all arms are identical
                if not (perm[0] == perm[1] == perm[2]):  
                    combination_name = "_".join(str(int(a * 1000) if a < 1 else int(a * 100)) for a in perm)
                    combinations_set.add((perm, combination_name))

    return list(combinations_set)  # Convert back to a list