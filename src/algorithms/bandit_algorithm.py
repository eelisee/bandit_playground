import csv

class BanditAlgorithm:
    def __init__(self, name):
        self.name = name
        self.results = []

    def add_result(self, param, iteration, total_reward, suboptimal_arms_count, total_regret, zeros_count, ones_count):
        self.results.append([param, iteration, total_reward, suboptimal_arms_count, round(total_regret, 2), zeros_count, ones_count])

    def save_results_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestep', 'Iteration', 'Total Reward', 'Suboptimal Arms', 'Total Regret', 'Zeros Count', 'Ones Count'])
            for result in self.results:
                writer.writerow(result)

    def calculate_average_results(self):
        avg_results = {}
        for result in self.results:
            param = result[0]
            if param not in avg_results:
                avg_results[param] = [0, 0, 0, 0, 0]
            avg_results[param][0] += result[2]  # Total Reward
            avg_results[param][1] += result[3]  # Suboptimal Arms Count
            avg_results[param][2] += result[4]  # Total Regret
            avg_results[param][3] += result[5]  # Zeros Count
            avg_results[param][4] += result[6]  # Ones Count

        for param in avg_results:
            avg_results[param] = [param] + [x / 100 for x in avg_results[param]]
        return list(avg_results.values())
    

        def calculate_average_results(self):
        time_steps = sorted(set(result[0] for result in self.results))
        avg_results = []
        for timestep in time_steps:
            total_reward_sum = 0
            suboptimal_arms_sum = 0
            regret_sum = 0
            zeros_count_sum = 0
            ones_count_sum = 0
            count = 0
            for result in self.results:
                if result[0] == timestep:
                    total_reward_sum += result[2]
                    suboptimal_arms_sum += result[3]
                    regret_sum += result[4]
                    zeros_count_sum += result[5]
                    ones_count_sum += result[6]
                    count += 1
            avg_total_reward = total_reward_sum / count if count > 0 else 0
            avg_suboptimal_arms = suboptimal_arms_sum / count if count > 0 else 0
            avg_regret = regret_sum / count if count > 0 else 0
            avg_zeros_count = zeros_count_sum / count if count > 0 else 0
            avg_ones_count = ones_count_sum / count if count > 0 else 0
            avg_results.append((timestep, avg_total_reward, avg_suboptimal_arms, avg_regret, avg_zeros_count, avg_ones_count))
        return avg_results