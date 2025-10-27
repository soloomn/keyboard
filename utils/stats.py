"""
Модуль с утилитами для обработки больших текстов и вывода результатов.

Содержит:
- analyze_large_file(): потоковый анализ текста частями;
- show_finger_stats(): формирование и красивый вывод статистики по пальцам.
"""

import pandas as pd
from pandas import DataFrame
from rich.console import Console
from rich.table import Table


def show_finger_stats(analyzer, layout_name: str = "qwer") -> DataFrame:
    """
    Формирует и красиво выводит статистику по пальцам с помощью pandas и rich.

    Parameters
    ----------
    analyzer : LayoutAnalyzer
        Объект анализатора с накопленной статистикой.
    layout_name : str, optional
        Имя раскладки для анализа (например: 'qwer', 'diktor', 'vyzov').

    Returns
    -------
    pandas.DataFrame
        Таблица с количеством нажатий и процентным распределением.
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
