import matplotlib
matplotlib.use("Agg")  # Без GUI

from visual import show_all

def test_show_all_smoke(monkeypatch):
    data = {"left": [1, 2, 3, 4, 5], "right": [5, 4, 3, 2, 1]}
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)
    show_all(data, data, data)