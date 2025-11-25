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
from pathlib import Path
from typing import Optional
from pandas import DataFrame
from rich.console import Console
from rich.table import Table

MARKER = "Статистика по выбранной раскладке"

def process_file(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

    result = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        result.append(line)

        # Если нашли строку с маркером — пропускаем 4 строки после неё
        if MARKER in line and i + 4 < n:
            i += 1  # перейдём на следующую
            result.append(lines[i])  # оставляем 1‑ю после маркера
            i += 1
            result.append(lines[i])  # оставляем 2‑ю после маркера
            i += 1
            result.append(lines[i])  # оставляем 3‑ю после маркера
            i += 1  # теперь на 4‑й строке (её пропускаем)
        i += 1

    path.write_text("".join(result), encoding="utf-8")

def show_finger_stats(analyzer,
                      layout_name: str = "qwer",
                      output_file: Optional[str] = "/app/data_output/output.txt") -> DataFrame:
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

    console_kwargs = {}
    if output_file:
        console_kwargs["file"] = open(output_file, 'a', encoding='utf-8')

    console = Console(**console_kwargs)

    console.print("=" * 80)
    console.print(f"Статистика по выбранной раскладке {layout_name}:")
    console.print("=" * 80)

    table = Table()

    table.add_column("Палец", justify="left")
    table.add_column("Нажатий", justify="right")
    table.add_column("Доля (%)", justify="right")

    for _, row in df.iterrows():
        table.add_row(str(row["finger"]),
                      str(row["presses"]),
                      f"{row['percent']:.2f}")

    console.print(table)

    if output_file and console.file:
        console.file.close()

    process_file(Path(output_file))

    return df
