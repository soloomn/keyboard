import pytest
from models.keyboard_analyzer import LayoutAnalyzer
from utils.stats import show_finger_stats

def test_finger_stats_calculation():
    analyzer = LayoutAnalyzer()
    # делаем реальный анализ на коротком тексте, чтобы stats были не пустые
    analyzer.analyze_text("Привет мир")
    stats_output = show_finger_stats(analyzer, "qwer")
    # теперь суммы должны быть > 0
    assert stats_output.sum(numeric_only=True).sum() > 0

def test_show_finger_stats_runs(capsys):
    analyzer = LayoutAnalyzer()
    show_finger_stats(analyzer, "qwer")
    output = capsys.readouterr().out
    assert "Палец" in output or "Finger" in output