import os
import pandas as pd
from config import algorithm_strategy_pairs, base_path
from utils.simulation_utils import get_directory_for_algorithm

# Iterate over all algorithms and their parameters
for algorithm, config in algorithm_strategy_pairs:
    # Get the directory for the current algorithm and parameters
    params = config.get("params", {})
    algorithm_dir = get_directory_for_algorithm(algorithm, params)
    
    # Iterate over all CSV files in the directory
    for root, _, files in os.walk(algorithm_dir):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                
                # Load the CSV file into a DataFrame
                df = pd.read_csv(file_path)
                
                # Identify and remove duplicate rows for Timestep 10000 in each iteration
                df_cleaned = df[~((df["Timestep"] == 10000) & (df.duplicated(subset=["Timestep", "Iteration"], keep="first")))]
                
                # Save the cleaned DataFrame back to the CSV file
                df_cleaned.to_csv(file_path, index=False)