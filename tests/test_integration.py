import pytest
from models import RedisStorage  # путь поправь, если модуль по-другому называется

@pytest.fixture(scope="module")
def storage():
    """Фикстура для подключения к Redis."""
    return RedisStorage()


def test_layouts_saved_to_redis(storage):
    """Проверяем, что данные раскладок записались в Redis в ожидаемом формате."""
    # ключ, под которым сохраняется словарь всех раскладок (должен совпадать с тем, что в коде analyzer)
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