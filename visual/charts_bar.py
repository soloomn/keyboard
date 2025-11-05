"""
Модуль для визуализации нагрузок на пальцы в виде горизонтальных гистограмм.

Содержит функцию plot_finger_usage_with_values для построения горизонтальных гистограмм,
сравнивающих распределение нагрузок на пальцы между различными клавиатурными раскладками.

Основные возможности:
- Сравнение нагрузок для 7 различных раскладок клавиатуры
- Визуализация данных в виде горизонтальных столбчатых диаграмм
- Отображение численных значений нагрузок непосредственно на графике
- Автоматическое сохранение результата в файл

Используемые библиотеки:
- matplotlib для построения графиков
- numpy для работы с числовыми массивами
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
    Строит горизонтальную гистограмму нагрузок по пальцам для семи раскладок клавиатуры.

    ВХОД:
        data_diktor (dict): Данные для раскладки "Диктор" в формате {'left': list, 'right': list}
        data_qwer (dict): Данные для раскладки "Йцукен" в формате {'left': list, 'right': list}
        data_vyzov (dict): Данные для раскладки "Вызов" в формате {'left': list, 'right': list}
        data_ant (dict): Данные для раскладки "Ант" в формате {'left': list, 'right': list}
        data_skoropis (dict): Данные для раскладки "Скоропись" в формате {'left': list, 'right': list}
        data_zubachew (dict): Данные для раскладки "Зубачев" в формате {'left': list, 'right': list}
        data_rusphone (dict): Данные для раскладки "РусФон" в формате {'left': list, 'right': list}

    Структура данных для каждой раскладки:
        - 'left': список из 5 значений нагрузок для пальцев левой руки
          [большой, указательный, средний, безымянный, мизинец]
        - 'right': список из 5 значений нагрузок для пальцев правой руки
          [большой, указательный, средний, безымянный, мизинец]

    ВЫХОД:
        None

    Действия функции:
        - Создает горизонтальную гистограмму с 10 группами столбцов (по 5 пальцев на каждую руку)
        - Отображает 7 наборов данных (по одному для каждой раскладки) разными цветами
        - Добавляет числовые значения нагрузок справа от каждого столбца в формате "Ш:{значение};"
        - Сохраняет график в файл '/app/data_output/charts_bar.png' с разрешением 300 DPI
        - Отображает легенду с названиями раскладок
        - Автоматически настраивает размеры и расположение элементов графика
        - Устанавливает заголовок "Сравнение нагрузок и штрафов на пальцы по раскладкам"
        - Настраивает оси: Y - названия пальцев, X - количество нажатий
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

    press_qwer = [val for pair in zip(data_qwer['left_press'], data_qwer['right_press']) for val in pair]
    press_diktor = [val for pair in zip(data_diktor['left_press'], data_diktor['right_press']) for val in pair]
    press_vyzov = [val for pair in zip(data_vyzov['left_press'], data_vyzov['right_press']) for val in pair]
    press_ant = [val for pair in zip(data_ant['left_press'], data_ant['right_press']) for val in pair]
    press_skoropis = [val for pair in zip(data_skoropis['left_press'], data_skoropis['right_press']) for val in pair]
    press_zubachew = [val for pair in zip(data_zubachew['left_press'], data_zubachew['right_press']) for val in pair]
    press_rusphone = [val for pair in zip(data_rusphone['left_press'], data_rusphone['right_press']) for val in pair]

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

    all_press = [
        press_qwer,
        press_rusphone,
        press_zubachew,
        press_skoropis,
        press_ant,
        press_vyzov,
        press_diktor
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
        current_press = all_press[i]
        current_color = colors[i]
        current_name = layout_names[i]

        current_offset = start_pos + i * bar_width

        rects = ax.barh(index + current_offset, current_layout, bar_width,
                        label=current_name, color=current_color, alpha=1.0)

        # --- Добавляем текст нагрузки и штрафов справа от каждого столбика ---
        for rect, press in zip(rects, current_press):
            width = rect.get_width()
            y_pos = rect.get_y() + rect.get_height() / 2

            text_to_display = f"Ш:{width:.0f}; Н:{press:.0f}"

            ax.text(width, y_pos, f" {text_to_display}",
                    va='center', ha='left', fontsize=5, color='black')

        current_max_load = max(current_layout)
        if current_max_load > max_total_load:
            max_total_load = current_max_load


    # Добавление подписей и заголовков
    ax.set_ylabel('Пальцы')
    ax.set_xlabel('Количество штрафов + количество нажатий')
    ax.set_title('Сравнение штрафов и нажатий на пальцы по раскладкам', fontsize=14, fontweight='bold')
    ax.set_yticks(index, fingers)  # Устанавливаем метки для оси Y

    ax.set_xlim(0, max_total_load * 1.25)

    ax.legend(loc='upper right')

    # Показ гистограммы
    plt.tight_layout()  # Автоматически корректирует параметры графика для плотного расположения
    plt.savefig('/app/data_output/charts_bar.png', dpi=300)