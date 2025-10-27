import json
import os
import pytest

# Путь внутри контейнера, куда analyzer пишет данные
DATA_PATH = "/app/data_output/layouts.json"

def test_layouts_file_created():
    """Проверяем, что файл JSON реально создан и содержит все раскладки"""
    assert os.path.exists(DATA_PATH), f"{DATA_PATH} не найден!"

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Проверяем ключи раскладок
    for layout in ["diktor", "qwer", "vyzov"]:
        assert layout in data, f"В layouts.json нет ключа {layout}"
        assert isinstance(data[layout], dict), f"{layout} не является словарем"
        assert "left" in data[layout] and "right" in data[layout], f"{layout} не содержит left/right"