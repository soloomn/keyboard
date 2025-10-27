import json
from unittest.mock import mock_open, patch

def test_show_all_with_mock():
    """Проверка функции show_all без реального файла"""
    fake_data = {
        "diktor": {"left": [1,2], "right": [3,4]},
        "qwer": {"left": [5,6], "right": [7,8]},
        "vyzov": {"left": [9,10], "right": [11,12]}
    }

    m = mock_open(read_data=json.dumps(fake_data))
    with patch("builtins.open", m):
        from visual.visualmain import show_all
        # Запускаем функцию с фейковыми данными
        show_all(fake_data["diktor"], fake_data["qwer"], fake_data["vyzov"])