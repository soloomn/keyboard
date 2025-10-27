import matplotlib
matplotlib.use("Agg")

from models import LayoutAnalyzer
from visual import show_all

def test_full_analysis_flow(monkeypatch):
    analyzer = LayoutAnalyzer()
    data = analyzer.reverser
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)
    show_all(data["diktor"], data["qwer"], data["vyzov"])