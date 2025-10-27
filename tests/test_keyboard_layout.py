import pytest
from models import KeyboardLayout

def test_keyboard_layout_initialization():
    layout = KeyboardLayout("Тестовая", "test")
    assert layout.name == "Тестовая"
    assert isinstance(layout.counter_fingers, dict)
    assert all(f'f{i}l' in layout.counter_fingers for i in range(1, 6))
    assert all(f'f{i}r' in layout.counter_fingers for i in range(1, 6))

def test_keyboard_layout_count_update():
    layout = KeyboardLayout("Тест", "test")
    initial_sum = sum(layout.counter_fingers.values())
    layout.counter_fingers["f1l"] += 10
    assert sum(layout.counter_fingers.values()) == initial_sum + 10