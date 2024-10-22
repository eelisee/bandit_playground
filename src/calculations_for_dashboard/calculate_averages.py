# # src/calculations_for_dashboard/calculate_averages.py

import os
import pandas as pd

# def calculate_average_and_save(algorithms, combinations, output_file_suffix, base_path):
#     """
#     Berechnet den Durchschnitt der Ergebnisse mehrerer Algorithmen und speichert die Ergebnisse.
    
#     :param algorithms: Liste der Algorithmennamen.
#     :param combinations: Liste der Dateikombinationen .
#     :param output_file_suffix: Suffix für die Output-Dateinamen.
#     :param base_path: Pfad, in dem die Algorithmen-Ergebnisse gespeichert sind.
#     """
#     for combination in combinations:
#         combined_df = None

#         for algorithm in algorithms:
#             file_path = os.path.join(base_path, f"{algorithm}_results_{combination}.csv")
#             if not os.path.exists(file_path):
#                 print(f"Datei nicht gefunden: {file_path}")
#                 continue
#             df = pd.read_csv(file_path)

#             if combined_df is None:
#                 combined_df = df
#             else:
#                 combined_df.iloc[:, 1:] += df.iloc[:, 1:]  # Addiere die Werte der entsprechenden Spalten

#         if combined_df is not None:
#             combined_df.iloc[:, 1:] /= len(algorithms)  # Berechne den Durchschnitt

#             output_file_path = os.path.join(base_path, f"{output_file_suffix}_results_{combination}.csv")
#             combined_df.to_csv(output_file_path, index=False)
#             print(f"Durchschnittswerte für {output_file_suffix} - {combination} erfolgreich gespeichert.")

# def run_average_calculations(algorithm_groups, combinations, base_path):
#     """
#     Führt die Durchschnittsberechnung für die definierten Algorithmengruppen durch.
    
#     :param algorithm_groups: Dictionary mit Gruppen von Algorithmen.
#     :param combinations: Liste der Dateikombinationen.
#     :param base_path: Basis-Pfad, in dem die Ergebnisse gespeichert sind.
#     """
#     for group_name, algorithms in algorithm_groups.items():
#         calculate_average_and_save(algorithms, combinations, group_name, base_path)

#     # Durchschnitt über die Iterationen für jede Gruppe berechnen
#         # for combination in combinations:
#         #     # Pfad zum durchschnittlichen Ergebnis für die Gruppe
#         #     avg_file_path = os.path.join(base_path, f"{group_name}_results_{combination}.csv")
#         #     if os.path.exists(avg_file_path):
#         #         df = pd.read_csv(avg_file_path)
#         #         calculate_average_and_save(group_name, combination, group_name, base_path)
#         #     else:
#         #         print(f"Datei nicht gefunden: {avg_file_path}")

#     for combination in combinations:
#         combined_df = None

#         for group_name in algorithm_groups.keys():
            
#             file_path = os.path.join(base_path, f"{group_name}_results_{combination}.csv")
#             if not os.path.exists(file_path):
#                 print(f"Datei nicht gefunden: {file_path}")
#                 continue
#             df = pd.read_csv(file_path)

#             if combined_df is None:
#                 combined_df = df
#             else:
#                 combined_df.iloc[:, 1:] += df.iloc[:, 1:]  # Addiere die Werte der entsprechenden Spalten

#         if combined_df is not None:
#             combined_df.iloc[:, 1:] /= len(algorithms)  # Berechne den Durchschnitt

#             output_file_path = os.path.join(base_path, f"{group_name}_average_results_{combination}.csv")
#             combined_df.to_csv(output_file_path, index=False)

def average_across_iterations(df, output_file_suffix, combination, base_path):
    """
    Berechnet den Durchschnitt über alle Iterationen für jede Zeitstufe und speichert die Ergebnisse.
    
    :param df: DataFrame mit den zusammengefassten Ergebnissen.
    :param output_file_suffix: Suffix für die Output-Dateinamen.
    :param combination: Die jeweilige Dateikombination (opt/subopt).
    :param base_path: Basispfad für das Speichern.
    """
    # Annahme: 'Timestep' ist die erste Spalte, und die Iterationen beginnen ab der zweiten Spalte
    timesteps = df['Timestep']
    avg_values = df.iloc[:, 1:].mean(axis=1)  # Berechne den Durchschnitt über alle Iterationen je Zeitstufe
    
    # Erstelle einen neuen DataFrame mit den Zeitstufen und Durchschnittswerten
    final_avg_df = pd.DataFrame({
        'Timestep': timesteps,
        'Average Regret': avg_values
    })

    # Speichere die finalen Durchschnittswerte in eine neue Datei
    final_output_path = os.path.join(base_path, f"Final_Averaged_{output_file_suffix}_results_{combination}.csv")
    final_avg_df.to_csv(final_output_path, index=False)
    print(f"Finale Durchschnittswerte erfolgreich gespeichert in: {final_output_path}")


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
            combined_df.iloc[:, 1:] /= len(algorithms)  # Berechne den Durchschnitt für alle Algorithmen

            # Speichere die Zwischenergebnisse pro Gruppe
            output_file_path = os.path.join(base_path, f"{output_file_suffix}_results_{combination}.csv")
            combined_df.to_csv(output_file_path, index=False)
            print(f"Durchschnittswerte für {output_file_suffix} - {combination} erfolgreich gespeichert.")

            # FINALER SCHRITT: Durchschnitt über die 100 Iterationen berechnen
            average_across_iterations(combined_df, output_file_suffix, combination, base_path)