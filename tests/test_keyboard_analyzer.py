import pytest
from models import LayoutAnalyzer


@pytest.fixture
def analyzer():
    return LayoutAnalyzer()


def test_layouts_initialized(analyzer):
    assert set(analyzer.layouts.keys()) == {'diktor', 'qwer', 'vyzov', 'ant', 'skoropis', 'rusphone', 'zubachew'}

    for layout in analyzer.layouts.values():
        assert hasattr(layout, 'counter_fingers')
        assert hasattr(layout, 'key_presses')
        assert hasattr(layout, 'hand_changes')


def test_reverser_returns_correct_structure(analyzer):

    reverser_data = analyzer.reverser
    assert isinstance(reverser_data, dict)
    assert ("diktor" in reverser_data
            and "qwer" in reverser_data
            and "vyzov" in reverser_data
            and "ant" in reverser_data
            and "skoropis" in reverser_data
            and "rusphone" in reverser_data
            and "zubachew" in reverser_data
            )

    for layout_key, layout_data in reverser_data.items():
        assert 'left' in layout_data and 'right' in layout_data
        assert len(layout_data['left']) == 5
        assert len(layout_data['right']) == 5


def test_format_coords_formats_correctly():
    res = LayoutAnalyzer.format_coords([1, 2], [3, 4])
    assert res == "(1,2)→(3,4)"
    assert LayoutAnalyzer.format_coords([], [1, 2]) == "N/A"


def test_analyze_text_updates_finger_loads(analyzer):
    analyzer.analyze_text("ПрИмер Текста")
    for layout in analyzer.layouts.values():
        total = layout.get_total_load
        assert isinstance(total, int)
        assert total > 0

        assert getattr(layout, 'counter_fingers', None) is not None
        assert getattr(layout, 'key_presses', None) is not None
        assert getattr(layout, 'hand_changes', None) is not None


def test_analyze_movement_details_returns_list(analyzer):
    info = analyzer.analyze_movement_details("тест", max_movements=3)
    assert isinstance(info, list)
    assert len(info) > 0
    move = info[0]
    assert 'from' in move and 'to' in move
    for layout_name in analyzer.layouts.keys():
        assert f'penalty_{layout_name}' in move
        assert f'finger_{layout_name}' in move
        assert f'pos_{layout_name}' in move
        assert f'move_type_{layout_name}' in move


def test_print_final_results_executes_without_errors(analyzer, capsys):
    analyzer.analyze_text("Пример текста")
    analyzer.print_final_results()
    captured = capsys.readouterr()
    assert "ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ" in captured.out
