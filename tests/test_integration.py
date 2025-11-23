"""
Модуль интеграционных тестов для проверки работы с Redis.

Содержит тесты для проверки корректности сохранения и загрузки данных
анализа клавиатурных раскладок в Redis хранилище.

Основные тесты:
- Проверка сохранения данных раскладок в Redis
- Проверка формата данных для всех поддерживаемых раскладок
- Проверка наличия обязательных полей в данных раскладок

Используемые библиотеки:
- pytest для организации тестирования
- models для работы с RedisStorage
"""

import pytest
import fakeredis

from models import RedisStorage

@pytest.fixture(scope="module")
def storage():
    data = {
        'diktor': {'left': [0, 0, 0, 0, 0], 'right': [0, 0, 0, 0, 0], 'two_handed': 0, 'left_press': [0, 0, 0, 0, 0],
                   'right_press': [0, 0, 0, 0, 0]},
        'qwer': {'left': [0, 0, 0, 0, 0], 'right': [0, 0, 0, 0, 0], 'two_handed': 0, 'left_press': [0, 0, 0, 0, 0],
                 'right_press': [0, 0, 0, 0, 0]},
        'vyzov': {'left': [0, 0, 0, 0, 0], 'right': [0, 0, 0, 0, 0], 'two_handed': 0, 'left_press': [0, 0, 0, 0, 0],
                  'right_press': [0, 0, 0, 0, 0]},
        'ant': {'left': [0, 0, 0, 0, 0], 'right': [0, 0, 0, 0, 0], 'two_handed': 0, 'left_press': [0, 0, 0, 0, 0],
                'right_press': [0, 0, 0, 0, 0]},
        'skoropis': {'left': [0, 0, 0, 0, 0], 'right': [0, 0, 0, 0, 0], 'two_handed': 0, 'left_press': [0, 0, 0, 0, 0],
                     'right_press': [0, 0, 0, 0, 0]},
        'rusphone': {'left': [0, 0, 0, 0, 0], 'right': [0, 0, 0, 0, 0], 'two_handed': 0, 'left_press': [0, 0, 0, 0, 0],
                     'right_press': [0, 0, 0, 0, 0]},
        'zubachew': {'left': [0, 0, 0, 0, 0], 'right': [0, 0, 0, 0, 0], 'two_handed': 0, 'left_press': [0, 0, 0, 0, 0],
                     'right_press': [0, 0, 0, 0, 0]}
    }

    s = RedisStorage()
    s.client = fakeredis.FakeRedis()
    s.save("layouts", data)
    return s


def test_layouts_saved_to_redis(storage):
    """
    Проверяем, что данные раскладок записались в Redis в ожидаемом формате.

    ВХОД:
        storage (RedisStorage): Фикстура с подключением к Redis

    ВЫХОД:
        None (тест проходит или падает с assertion error)

    Проверки:
        - Наличие данных по ключу "layouts" в Redis
        - Присутствие всех 7 поддерживаемых раскладок в данных
        - Корректность структуры данных для каждой раскладки
        - Наличие обязательных полей: left, right, two_handed
    """
    key = "layouts"

    data = storage.load(key)
    assert data is not None, f"В Redis нет данных по ключу {key}"

    # проверяем наличие основных раскладок
    for layout in ["diktor", "qwer", "vyzov", "ant", "skoropis", "rusphone", "zubachew"]:
        assert layout in data, f"В данных Redis отсутствует раскладка {layout}"
        layout_data = data[layout]
        assert isinstance(layout_data, dict), f"{layout} не является словарём"
        assert "left" in layout_data, f"В {layout} нет ключа left"
        assert "right" in layout_data, f"В {layout} нет ключа right"
        assert "two_handed" in layout_data, f"В {layout} нет ключа two_handed"