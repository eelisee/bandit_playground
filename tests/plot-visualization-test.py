import os
import pytest
import pandas as pd
from dash.testing.application_runners import import_app

@pytest.fixture
def dash_app():
    # load Dashboard
    app = import_app('dashboard')
    return app

def test_csv_loading_and_plots(dash_duo, dash_app):
    # Start App
    dash_duo.start_server(dash_app)

    # Test if CSV are available
    base_path = os.path.join(os.getcwd(), "data", "algorithms_results")
    
    # List of files to check
    files_to_check = [
        "1_ETC_average_results_opt_ver1.csv",
        "2_Greedy_average_results_opt_ver1.csv",
        # insert here other file names
    ]
    
    # Test, if files exist
    for file_name in files_to_check:
        file_path = os.path.join(base_path, file_name)
        assert os.path.exists(file_path), f"{file_name} does not exist. Check whether the file has been moved correctly and is located in the 'data/algorithms_results' directory."
        
        # Testen, ob die CSV-Dateien gelesen werden können
        df = pd.read_csv(file_path)
        assert not df.empty, f"{file_name} could not be loaded. Check manually wether the file can be read."
    
    # Teste, ob das Dashboard die Plots rendert
    dash_duo.wait_for_element("#plot-area", timeout=10)  # Hier sollte die ID des Plot-Bereichs stehen
    assert dash_duo.find_element("#plot-area") is not None
