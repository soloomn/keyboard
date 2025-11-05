"""
Модуль unit-тестов для класса KeyboardLayout.

Содержит тесты для проверки корректности работы клавиатурных раскладок,
включая инициализацию, расчет штрафов, распределение нагрузки и другие функции.

Основные тесты:
- Проверка инициализации раскладок
- Тестирование определения полей символов для разных раскладок
- Проверка расчета штрафов за перемещения
- Тестирование распределения нагрузки по пальцам
- Проверка обработки пробелов и заглавных букв
- Тестирование определения типов перемещений

Используемые библиотеки:
- pytest для организации тестирования
- models для работы с KeyboardLayout
"""

import pytest
from models import KeyboardLayout


@pytest.fixture
def qwer_layout():
    """
    Фикстура для создания раскладки ЙЦУКЕН.

    ВХОД: Нет

    ВЫХОД:
        KeyboardLayout: Экземпляр раскладки ЙЦУКЕН
    """
    return KeyboardLayout("ЙЦУКЕН", "qwer")


@pytest.fixture
def vyzov_layout():
    """
    Фикстура для создания раскладки Вызов.

    ВХОД: Нет

    ВЫХОД:
        KeyboardLayout: Экземпляр раскладки Вызов
    """
    return KeyboardLayout("Вызов", "vyzov")


@pytest.fixture
def test_layout():
    """
    Фикстура для создания тестовой раскладки.

    ВХОД: Нет

    ВЫХОД:
        KeyboardLayout: Экземпляр тестовой раскладки
    """
    return KeyboardLayout("Тестовая", "test")


def test_keyboard_layout_initialization(test_layout):
    """
    Проверяет корректность инициализации раскладки.

    ВХОД:
        test_layout (KeyboardLayout): Фикстура тестовой раскладки

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    assert test_layout.name == "Тестовая"
    assert isinstance(test_layout.counter_fingers, dict)
    assert all(f'f{i}l' in test_layout.counter_fingers for i in range(1, 6))
    assert all(f'f{i}r' in test_layout.counter_fingers for i in range(1, 6))


def test_keyboard_layout_count_update(test_layout):
    """
    Проверяет корректность обновления счетчиков нагрузки.

    ВХОД:
        test_layout (KeyboardLayout): Фикстура тестовой раскладки

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    initial_sum = sum(test_layout.counter_fingers.values())
    test_layout.counter_fingers["f1l"] += 10
    assert sum(test_layout.counter_fingers.values()) == initial_sum + 10


def test_get_symbol_field_for_different_layouts():
    """
    Проверяет корректность определения полей символов для всех раскладок.

    ВХОД: Нет

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    assert KeyboardLayout("Диктор", "diktor").get_symbol_field == "key"
    assert KeyboardLayout("ЙЦУКЕН", "qwer").get_symbol_field == "qwer"
    assert KeyboardLayout("Вызов", "vyzov").get_symbol_field == "vyzov"
    assert KeyboardLayout("ант","ant").get_symbol_field == "ant"
    assert KeyboardLayout("скоропись", "skoropis").get_symbol_field == "skoropis"
    assert KeyboardLayout("русфон", "rusphone").get_symbol_field == "rusphone"
    assert KeyboardLayout("зубачев", "zubachew").get_symbol_field == "zubachew"


def test_calculate_penalty_variants():
    """
    Проверяет корректность расчета штрафов для различных типов перемещений.

    ВХОД: Нет

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    assert KeyboardLayout.calculate_penalty([1, 2], [1, 2]) == 0
    assert KeyboardLayout.calculate_penalty([1, 2], [2, 2]) == 1
    assert KeyboardLayout.calculate_penalty([1, 2], [2, 3]) == 2
    assert KeyboardLayout.calculate_penalty([0, 0], [3, 4]) in (3, 4)


def test_get_finger_by_column_correct_mapping():
    """
    Проверяет корректность сопоставления колонок с пальцами.

    ВХОД: Нет

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    layout = KeyboardLayout("Диктор", "diktor")
    assert layout.get_finger_by_column(0) == 'f5l'
    assert layout.get_finger_by_column(4) == 'f2l'
    assert layout.get_finger_by_column(8) == 'f3r'
    assert layout.get_finger_by_column(12) == 'f5r'


def test_apply_finger_load_increments_properly(qwer_layout):
    """
    Проверяет корректность применения нагрузки к пальцам.

    ВХОД:
        qwer_layout (KeyboardLayout): Фикстура раскладки ЙЦУКЕН

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    qwer_layout.apply_finger_load(8, 2)
    assert qwer_layout.counter_fingers['f3r'] == 2


def test_count_spaces_distribution(qwer_layout, vyzov_layout):
    """
    Проверяет корректность распределения нагрузки от пробелов.

    ВХОД:
        qwer_layout (KeyboardLayout): Фикстура раскладки ЙЦУКЕН
        vyzov_layout (KeyboardLayout): Фикстура раскладки Вызов

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    qwer_layout.count_spaces(10)
    vyzov_layout.count_spaces(10)
    assert qwer_layout.counter_fingers['f1l'] == 6
    assert qwer_layout.counter_fingers['f1r'] == 4
    assert vyzov_layout.counter_fingers['f1l'] == 5
    assert vyzov_layout.counter_fingers['f1r'] == 5


def test_add_uppercase_penalty_adds_penalty_to_left_thumb(qwer_layout):
    """
    Проверяет корректность применения штрафа за заглавные буквы.

    ВХОД:
        qwer_layout (KeyboardLayout): Фикстура раскладки ЙЦУКЕН

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    qwer_layout.add_uppercase_penalty(3)
    assert qwer_layout.counter_fingers['f5l'] == 6


def test_get_total_and_finger_load(qwer_layout):
    """
    Проверяет корректность расчета общей и пальцевой нагрузки.

    ВХОД:
        qwer_layout (KeyboardLayout): Фикстура раскладки ЙЦУКЕН

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    qwer_layout.counter_fingers['f2r'] = 7
    qwer_layout.counter_fingers['f4r'] = 3
    assert qwer_layout.get_finger_load('f2r') == 7
    assert qwer_layout.get_total_load == 10


def test_get_movement_type_various_cases():
    """
    Проверяет корректность определения типов перемещений.

    ВХОД: Нет

    ВЫХОД:
        None (тест проходит или падает с assertion error)
    """
    assert KeyboardLayout.get_movement_type([1, 1], [1, 1]) == "Та же клавиша"
    assert KeyboardLayout.get_movement_type([1, 1], [2, 1]) == "Вертикаль (1)"
    assert KeyboardLayout.get_movement_type([1, 1], [1, 2]) == "Горизонталь (1)"
    assert KeyboardLayout.get_movement_type([1, 1], [2, 2]) == "Диагональ (2)"
    assert "Сложное" in KeyboardLayout.get_movement_type([0, 0], [3, 4])
