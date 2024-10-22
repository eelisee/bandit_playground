import csv
from collections import defaultdict

class BanditAlgorithm:
    def __init__(self, name):
        self.name = name
        self.results = []

    def add_result(self, param, iteration, total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count):
        self.results.append([param, iteration, total_reward, suboptimal_arms_count, round(total_regret, 2), zeros_count, ones_count])
        # Print the added result to verify
        print(f"Added result: {[param, iteration, total_reward, suboptimal_arms_count, round(total_regret, 2), zeros_count, ones_count]}")

        # Optional: Raise an error if the result is not added (for debugging purposes)
        if [param, iteration, total_reward, suboptimal_arms_count, round(total_regret, 2), zeros_count, ones_count] not in self.results:
            raise ValueError("Result was not added to the results list.")

    def save_results_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestep', 'Iteration', 'Total Reward', 'Suboptimal Arms', 'Total Regret', 'Zeros Count', 'Ones Count'])
            for result in self.results:
                writer.writerow(result)

    def calculate_average_results(self):
        time_step_data = defaultdict(lambda: [0, 0, 0, 0, 0, 0])    
        time_step_counts = defaultdict(int)

        for result in self.results:
            timestep = result[0]
            time_step_data[timestep][0] += result[2]  # Total Reward
            time_step_data[timestep][1] += result[3]  # Suboptimal Arms Count
            time_step_data[timestep][2] += result[4]  # Total Regret
            time_step_data[timestep][3] += result[5]  # Zeros Count
            time_step_data[timestep][4] += result[6]  # Ones Count
            time_step_counts[timestep] += 1

        avg_results = []
        for timestep, data in time_step_data.items():
            count = time_step_counts[timestep]
            avg_results.append((
            timestep,
            data[0] / count if count > 0 else 0,
            data[1] / count if count > 0 else 0,
            data[2] / count if count > 0 else 0,
            data[3] / count if count > 0 else 0,
            data[4] / count if count > 0 else 0
            ))

        return sorted(avg_results, key=lambda x: x[0])
        