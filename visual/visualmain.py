"""
Модуль-агрегатор для отображения всех визуализаций анализа раскладок.

Содержит функцию show_all, которая последовательно вызывает все доступные
графические функции для комплексного визуального анализа данных
по клавиатурным раскладкам.

Основные возможности:
- Последовательное отображение 4 типов графиков анализа
- Загрузка данных из Redis хранилища
- Комплексная визуализация всех аспектов эргономики раскладок

Используемые модули:
- visual: для построения различных типов графиков
- models: для работы с Redis хранилищем
- json: для работы с данными (закомментировано)
"""

import json
from visual import plot_finger_usage_with_values
from visual import plot_only_pie_charts
from visual import plot_finger_loads_by_layout
from visual import create_total_load_pie_chart
from models import RedisStorage


def show_all(data_diktor: dict, data_qwer: dict, data_vyzov: dict,
             data_ant: dict, data_skoropis: dict, data_zubachew: dict, data_rusphone: dict) -> None:
    """
    Последовательно отображает все доступные визуализации для анализа раскладок.

    ВХОД:
        data_diktor (dict): Данные для раскладки "Диктор" в формате {'left': list, 'right': list}
        data_qwer (dict): Данные для раскладки "Йцукен" в формате {'left': list, 'right': list}
        data_vyzov (dict): Данные для раскладки "Вызов" в формате {'left': list, 'right': list}
        data_ant (dict): Данные для раскладки "Ант" в формате {'left': list, 'right': list}
        data_skoropis (dict): Данные для раскладки "Скоропись" в формате {'left': list, 'right': list}
        data_zubachew (dict): Данные для раскладки "Зубачев" в формате {'left': list, 'right': list}
        data_rusphone (dict): Данные для раскладки "РусФон" в формате {'left': list, 'right': list}

    ВЫХОД:
        None (последовательно отображает 4 типа графиков с помощью matplotlib)

    Действия функции:
        - Строит горизонтальные гистограммы нагрузок на пальцы
        - Создает круговые диаграммы распределения нагрузок на руки
        - Отображает множественные графики нагрузок по типам пальцев
        - Строит сводную круговую диаграмму общей нагрузки
    """
    plot_finger_usage_with_values(data_diktor, data_qwer, data_vyzov, data_ant, data_skoropis, data_zubachew, data_rusphone)
    plot_only_pie_charts(data_diktor, data_qwer, data_vyzov, data_ant, data_skoropis, data_zubachew, data_rusphone)
    plot_finger_loads_by_layout(data_diktor, data_qwer, data_vyzov, data_ant, data_skoropis, data_zubachew, data_rusphone)
    create_total_load_pie_chart(data_diktor, data_qwer, data_vyzov)

# загружаем данные из JSON
#with open("/app/data_output/layouts.json", "r", encoding="utf-8") as f:
     #data = json.load(f)

storage = RedisStorage()
data = storage.load("layouts")

show_all(data['diktor'], data['qwer'], data['vyzov'], data['ant'], data['skoropis'], data['zubachew'], data['rusphone'])