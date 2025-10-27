"""
keyboard — пакет для анализа раскладок клавиатуры.
Содержит:
 - KeyboardLayout — универсальная модель клавиатуры;
 - LayoutAnalyzer — инструмент анализа текста;
 - data_dict — исходные данные клавиатурных раскладок.
"""

from .models import KeyboardLayout, LayoutAnalyzer
from .data import data_dict

__all__ = ["KeyboardLayout", "LayoutAnalyzer", "data_dict"]