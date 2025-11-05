"""
Модуль unit-тестов для утилитных функций статистики.

Содержит тесты для проверки корректности работы функций статистики,
включая расчет нагрузок на пальцы и вывод форматированных результатов.

Основные тесты:
- Проверка расчета статистики нагрузок на пальцы
- Проверка корректности вывода статистики
- Тестирование работы с реальными данными анализа

Используемые библиотеки:
- pytest для организации тестирования
- models для работы с LayoutAnalyzer
- utils для тестируемых функций статистики
"""

import pytest
from models import LayoutAnalyzer
from utils import show_finger_stats


@pytest.fixture
def analyzer():
    """
    Фикстура для создания экземпляра LayoutAnalyzer.

    ВХОД: Нет

    ВЫХОД:
        LayoutAnalyzer: Экземпляр анализатора для тестирования
    """
    return LayoutAnalyzer()


def test_finger_stats_calculation(analyzer):
    """
    Проверяет корректность расчета статистики нагрузок на пальцы.

    ВХОД:
        analyzer (LayoutAnalyzer): Фикстура анализатора

    ВЫХОД:
        None (тест проходит или падает с assertion error)

    Действия:
        - Выполняет анализ короткого текста для генерации данных
        - Получает статистику для раскладки ЙЦУКЕН
        - Проверяет, что суммарные значения нагрузки больше 0
    """
    # делаем реальный анализ на коротком тексте, чтобы stats были не пустые
    analyzer.analyze_text("Привет мир")
    stats_output = show_finger_stats(analyzer, "qwer")
    # теперь суммы должны быть > 0
    assert stats_output.sum(numeric_only=True).sum() > 0


def test_show_finger_stats_runs(capsys, analyzer):
    """
    Проверяет корректность вывода статистики в консоль.

    ВХОД:
        capsys: Фикстура pytest для перехвата вывода
        analyzer (LayoutAnalyzer): Фикстура анализатора

    ВЫХОД:
        None (тест проходит или падает с assertion error)

    Действия:
        - Вызывает функцию show_finger_stats
        - Перехватывает вывод в консоль
        - Проверяет наличие ожидаемых заголовков в выводе
    """
    show_finger_stats(analyzer, "qwer")
    output = capsys.readouterr().out
    assert "Палец" in output or "Finger" in output