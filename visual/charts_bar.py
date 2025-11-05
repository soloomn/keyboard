"""
Модуль для визуализации нагрузок на пальцы в виде гистограмм.

Содержит функцию plot_finger_usage_with_values для построения горизонтальных гистограмм,
сравнивающих распределение нагрузок на пальцы между различными клавиатурными раскладками.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_finger_usage_with_values(data_diktor: dict,
                                  data_qwer: dict,
                                  data_vyzov: dict,
                                  data_ant: dict,
                                  data_skoropis: dict,
                                  data_zubachew: dict,
                                  data_rusphone: dict) -> None:
    """
    Строит горизонтальную гистограмму нагрузок по пальцам для трёх раскладок.

    ВХОД:
        data_diktor (dict): Данные для раскладки "Диктор" в формате {'left': list, 'right': list}
        data_qwer (dict): Данные для раскладки "Йцукен" в формате {'left': list, 'right': list}
        data_vyzov (dict): Данные для раскладки "Вызов" в формате {'left': list, 'right': list}

    ВЫХОД: Нет (отображает интерактивную гистограмму с помощью matplotlib)
    """
    fingers = [
        'Л_Большой', 'П_Большой',
        'Л_Указательный', 'П_Указательный',
        'Л_Средний', 'П_Средний',
        'Л_Безымянный', 'П_Безымянный',
        'Л_Мизинец', 'П_Мизинец'
    ]

    # Преобразуем словари в плоские списки
    layout_qwer = [val for pair in zip(data_qwer['left'], data_qwer['right']) for val in pair]
    layout_diktor = [val for pair in zip(data_diktor['left'], data_diktor['right']) for val in pair]
    layout_vyzov = [val for pair in zip(data_vyzov['left'], data_vyzov['right']) for val in pair]
    layout_ant = [val for pair in zip(data_ant['left'], data_ant['right']) for val in pair]
    layout_skoropis = [val for pair in zip(data_skoropis['left'], data_skoropis['right']) for val in pair]
    layout_zubachew = [val for pair in zip(data_zubachew['left'], data_zubachew['right']) for val in pair]
    layout_rusphone = [val for pair in zip(data_rusphone['left'], data_rusphone['right']) for val in pair]

    # Цвета для раскладок
    colors = ["#FF0000",  # Красный для Йцукен
              "#FFC0CB",  # Розовый
              "#9467bd",  # Фиолетовый
              "#008000",  # Зеленый
              "#0000FF",  # Голубой
              "#000000",  # Чёрный для Вызов
              "#FBFF00"  # Жёлтый для Диктор
    ]

    all_layouts = [
        layout_qwer,
        layout_rusphone,
        layout_zubachew,
        layout_skoropis,
        layout_ant,
        layout_vyzov,
        layout_diktor
    ]

    layout_names = ['Йцукен', 'РусФон', 'Зубачев', 'Скоропись', 'Ант', 'Вызов', 'Диктор']

    # Позиции столбцов на оси Y
    index = np.arange(len(fingers))

    # Ширина столбцов. Сделаем ее немного меньше, чтобы было место для текста.
    bar_width = 0.12

    total_width = len(all_layouts) * bar_width
    start_pos = -total_width / 2 + bar_width / 2

    # Построение горизонтальной гистограммы
    # plt.barh возвращает список объектов `Rectangle` (прямоугольники, т.е. столбцы)
    fig, ax = plt.subplots(figsize=(14, 10))

    max_total_load = 0

    for i in range(len(all_layouts)):
        current_layout = all_layouts[i]
        current_color = colors[i]
        current_name = layout_names[i]

        current_offset = start_pos + i * bar_width

        rects = ax.barh(index + current_offset, current_layout, bar_width,
                        label=current_name, color=current_color, alpha=1.0)

        # --- Добавляем текст нагрузки и штрафов справа от каждого столбика ---
        for rect in rects:
            width = rect.get_width()
            y_pos = rect.get_y() + rect.get_height() / 2

            text_to_display = f"Ш:{width:.0f};"

            ax.text(width, y_pos, f" {text_to_display}",
                    va='center', ha='left', fontsize=5, color='black')

        current_max_load = max(current_layout)
        if current_max_load > max_total_load:
            max_total_load = current_max_load


    # Добавление подписей и заголовков
    ax.set_ylabel('Пальцы')
    ax.set_xlabel('Нагрузки (количество нажатий)')
    ax.set_title('Сравнение нагрузок и штрафов на пальцы по раскладкам', fontsize=14, fontweight='bold')
    ax.set_yticks(index, fingers)  # Устанавливаем метки для оси Y

    ax.set_xlim(0, max_total_load * 1.25)

    ax.legend(loc='upper right')

    # Показ гистограммы
    plt.tight_layout()  # Автоматически корректирует параметры графика для плотного расположения
    plt.savefig('/app/data_output/charts_bar.png', dpi=300)