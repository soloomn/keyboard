"""
Модуль-агрегатор для отображения всех визуализаций анализа раскладок.

Содержит функцию show_all, которая последовательно вызывает все доступные
графические функции для комплексного визуального анализа данных
по клавиатурным раскладкам.
"""

import json
from visual import plot_finger_usage_with_values
from visual import plot_only_pie_charts
from visual import plot_finger_loads_by_layout
from visual import create_total_load_pie_chart


def show_all(data_diktor: dict, data_qwer: dict, data_vyzov: dict,
             data_ant: dict, data_skoropis: dict, data_zubachew: dict, data_rusphone: dict) -> None:
    """
    Последовательно отображает все доступные визуализации для анализа раскладок.

    ВХОД:
        data_diktor (dict): Данные для раскладки "Диктор" в формате {'left': list, 'right': list}
        data_qwer (dict): Данные для раскладки "Йцукен" в формате {'left': list, 'right': list}
        data_vyzov (dict): Данные для раскладки "Вызов" в формате {'left': list, 'right': list}

    ВЫХОД: Нет (последовательно отображает 4 типа графиков с помощью matplotlib)
    """
    plot_finger_usage_with_values(data_diktor, data_qwer, data_vyzov, data_ant, data_skoropis, data_zubachew, data_rusphone)
    plot_only_pie_charts(data_diktor, data_qwer, data_vyzov, data_ant, data_skoropis, data_zubachew, data_rusphone)
    plot_finger_loads_by_layout(data_diktor, data_qwer, data_vyzov, data_ant, data_skoropis, data_zubachew, data_rusphone)
    create_total_load_pie_chart(data_diktor, data_qwer, data_vyzov)

# загружаем данные из JSON
with open("/app/data_output/layouts.json", "r", encoding="utf-8") as f:
     data = json.load(f)

show_all(data['diktor'], data['qwer'], data['vyzov'], data['ant'], data['skoropis'], data['zubachew'], data['rusphone'])