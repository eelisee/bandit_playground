# src/calculations_for_dashboard/calculate_averages.py

import os
import pandas as pd

def calculate_average_and_save(algorithms, combinations, output_file_suffix, base_path):
    """
    Berechnet den Durchschnitt der Ergebnisse mehrerer Algorithmen und speichert die Ergebnisse.
    
    :param algorithms: Liste der Algorithmennamen.
    :param combinations: Liste der Dateikombinationen (z.B. opt_ver1, subopt_ver1, etc.).
    :param output_file_suffix: Suffix für die Output-Dateinamen.
    :param base_path: Pfad, in dem die Algorithmen-Ergebnisse gespeichert sind.
    """
    for combination in combinations:
        combined_df = None

        for algorithm in algorithms:
            file_path = os.path.join(base_path, f"{algorithm}_results_{combination}.csv")
            if not os.path.exists(file_path):
                print(f"Datei nicht gefunden: {file_path}")
                continue
            df = pd.read_csv(file_path)

            if combined_df is None:
                combined_df = df
            else:
                combined_df.iloc[:, 1:] += df.iloc[:, 1:]  # Addiere die Werte der entsprechenden Spalten

        if combined_df is not None:
            combined_df.iloc[:, 1:] /= len(algorithms)  # Berechne den Durchschnitt

            output_file_path = os.path.join(base_path, f"{output_file_suffix}_results_{combination}.csv")
            combined_df.to_csv(output_file_path, index=False)
            print(f"Durchschnittswerte für {output_file_suffix} - {combination} erfolgreich gespeichert.")

def run_average_calculations(algorithm_groups, combinations, base_path):
    """
    Führt die Durchschnittsberechnung für die definierten Algorithmengruppen durch.
    
    :param algorithm_groups: Dictionary mit Gruppen von Algorithmen.
    :param combinations: Liste der Dateikombinationen.
    :param base_path: Basis-Pfad, in dem die Ergebnisse gespeichert sind.
    """
    for group_name, algorithms in algorithm_groups.items():
        calculate_average_and_save(algorithms, combinations, group_name, base_path)