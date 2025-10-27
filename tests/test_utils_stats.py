from models.keyboard_analyzer import LayoutAnalyzer
from utils.stats import show_finger_stats

def test_show_finger_stats_runs(capsys):
    analyzer = LayoutAnalyzer()
    show_finger_stats(analyzer, "qwer")
    output = capsys.readouterr().out
    assert "Палец" in output or "Finger" in output