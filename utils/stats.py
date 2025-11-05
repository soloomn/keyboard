"""
Модуль с утилитами для красивого вывода результатов.

Содержит функции для визуализации статистики анализа клавиатурных раскладок
с использованием библиотек pandas и rich для создания форматированных таблиц.

Основные возможности:
- Форматированный вывод статистики по нагрузке на пальцы
- Создание красивых таблиц с использованием rich
- Расчет процентного распределения нагрузки

Используемые библиотеки:
- pandas для работы с табличными данными
- rich для красивого вывода в консоль
"""

import pandas as pd
from pandas import DataFrame
from rich.console import Console
from rich.table import Table


def show_finger_stats(analyzer, layout_name: str = "qwer") -> DataFrame:
    """
    Формирует и красиво выводит статистику по пальцам с помощью pandas и rich.

    ВХОД:
        analyzer (LayoutAnalyzer): Объект анализатора с накопленной статистикой
        layout_name (str, optional): Имя раскладки для анализа
                                   ('qwer', 'diktor', 'vyzov', 'ant', 'skoropis', 'rusphone', 'zubachew')
                                   (по умолчанию "qwer")

    ВЫХОД:
        pandas.DataFrame: Таблица с данными о нагрузке на пальцы, содержащая колонки:
            - finger: идентификатор пальца
            - presses: количество нажатий
            - percent: процентное распределение нагрузки

    Действия функции:
        - Извлекает данные о нагрузке на пальцы для указанной раскладки
        - Создает DataFrame с количеством нажатий для каждого пальца
        - Рассчитывает процентное распределение нагрузки
        - Сортирует данные по убыванию количества нажатий
        - Выводит форматированную таблицу с использованием rich
        - Возвращает DataFrame для дальнейшего использования
    """
    layout = analyzer.layouts[layout_name]

    df = pd.DataFrame([
        {"finger": finger, "presses": count}
        for finger, count in layout.counter_fingers.items()
    ])
    df["percent"] = df["presses"] / df["presses"].sum() * 100
    df = df.sort_values("presses", ascending=False)

    console = Console()
    table = Table(title=f"Нагрузка по пальцам ({layout_name.upper()})")

    table.add_column("Палец", justify="left")
    table.add_column("Нажатий", justify="right")
    table.add_column("Доля (%)", justify="right")

    for _, row in df.iterrows():
        table.add_row(str(row["finger"]), str(row["presses"]), f"{row['percent']:.2f}")

    console.print(table)

    return df
