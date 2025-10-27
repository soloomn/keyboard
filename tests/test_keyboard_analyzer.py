from models import LayoutAnalyzer

def test_reverser_structure():
    analyzer = LayoutAnalyzer()
    data = analyzer.reverser

    assert isinstance(data, dict)
    assert "diktor" in data and "qwer" in data and "vyzov" in data

    for layout_data in data.values():
        assert "left" in layout_data and "right" in layout_data
        assert len(layout_data["left"]) == 5
        assert len(layout_data["right"]) == 5