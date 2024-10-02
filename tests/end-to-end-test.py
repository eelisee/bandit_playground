import pytest
from dash.testing.application_runners import import_app

@pytest.fixture
def dash_app():
    # Hier wird das Dashboard geladen
    app = import_app('dashboard')  # "dashboard" ist der Name der Python-Datei ohne .py
    return app

def test_dashboard_loading(dash_duo, dash_app):
    # Startet das Dashboard
    dash_duo.start_server(dash_app)
    
    # Überprüft, ob das Dashboard erfolgreich geladen wurde
    dash_duo.wait_for_page(dash_duo.server_url, timeout=10)
    
    # Überprüft, ob der Titel der Seite korrekt angezeigt wird
    assert dash_duo.driver.title == "Simulation of variance-aware Algorithms for Stochastic Bandit Problems"
    
    # Optional: Überprüft, ob das Layout (bestimmte Elemente) vorhanden ist
    assert dash_duo.find_element("body") is not None
