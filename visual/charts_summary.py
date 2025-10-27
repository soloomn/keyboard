"""
Модуль для построения сводной круговой диаграммы общей нагрузки.

Содержит функцию create_total_load_pie_chart для визуализации общего распределения
нагрузки между тремя клавиатурными раскладками в виде одной круговой диаграммы
с процентным соотношением и выделением сегментов.
"""

import matplotlib.pyplot as plt
import numpy as np


def create_total_load_pie_chart(data_diktor: dict,
                                data_qwer: dict,
                                data_vyzov: dict) -> None:
    """
    Строит одну круговую диаграмму общей нагрузки по трём раскладкам.

    ВХОД:
        data_diktor (dict): Данные для раскладки "Диктор" в формате {'left': list, 'right': list}
        data_qwer (dict): Данные для раскладки "Йцукен" в формате {'left': list, 'right': list}
        data_vyzov (dict): Данные для раскладки "Вызов" в формате {'left': list, 'right': list}

    ВЫХОД: Нет (отображает круговую диаграмму с помощью matplotlib)
    """
    values = [
        sum(data_qwer['left']) + sum(data_qwer['right']),
        sum(data_diktor['left']) + sum(data_diktor['right']),
        sum(data_vyzov['left']) + sum(data_vyzov['right']),
    ]
    labels = ['ЙЦУКЕН', 'ДИКТОР', 'ВЫЗОВ']
    colors = ['#FF0000', '#FBFF00', '#000000']
    offset_factor = 0.3

    # 1. Расчет общего значения и процентов
    total = sum(values)
    if total == 0:
        plt.figure(figsize=(4, 3))
        plt.text(0.5, 0.5, "Нет данных", ha="center", va="center", fontsize=12)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
        return

    percentages = [(v / total) * 100 for v in values]

    # 2. Создание фигуры и осей для графика
    fig, ax = plt.subplots(figsize=(8, 8))

    # 3. Построение круговой диаграммы.
    wedges, texts, _ = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct='',
        startangle=90,
        pctdistance = 0.85,
        explode = (0, 0, 0.1),  # Выдвигаем последний сегмент (ВЫЗОВ)
    )

    # 4. Добавление процентов как отдельных текстовых меток.

    for i, wedge in enumerate(wedges):
        # Получаем позицию метки (labels)
        x_label_pos, y_label_pos = texts[i].get_position()

        # Получаем текущий радиус позиции метки
        current_label_radius = np.sqrt(x_label_pos ** 2 + y_label_pos ** 2)

        # Определяем, куда "уходит" метка.
        # Если метка находится снаружи (достаточно далеко от центра),
        # мы рассчитываем новую позицию для процента, смещая ее вдоль радиуса метки.

        # Значение `threshold_radius` определяет, когда метка считается "снаружи".
        # Можно подобрать это значение. Например, 0.5 - это половина радиуса диаграммы.
        threshold_radius = 0.5

        if current_label_radius > threshold_radius:
            # Рассчитываем вектор направления от центра (0,0) к метке
            direction_x = x_label_pos / current_label_radius
            direction_y = y_label_pos / current_label_radius

            # Рассчитываем смещение. Это должно быть пропорционально радиусу метки.
            # Чем дальше метка, тем больше может быть смещение, но не слишком много,
            # чтобы проценты не разлетались далеко.
            # `(current_label_radius * 0.5)` - это попытка сделать смещение масштабируемым.
            # `offset_factor` - главный множитель, который мы будем менять.
            offset_distance = direction_x * offset_factor * (current_label_radius * 0.5)

            x_pos_percentage = x_label_pos + offset_distance
            y_pos_percentage = y_label_pos + offset_distance

        else:
            # Если метка оказалась очень близко к центру (редкий случай для labels),
            # используем тригонометрию для расчета позиции, но с большим множителем радиуса,
            # чтобы проценты были снаружи.
            center_angle_rad = np.deg2rad((wedge.theta1 + wedge.theta2) / 2)
            radius_for_percentage = 1.15  # Фиксированный множитель радиуса
            x_pos_percentage = radius_for_percentage * np.cos(center_angle_rad)
            y_pos_percentage = radius_for_percentage * np.sin(center_angle_rad)

        # Добавляем текстовый элемент с процентом
        ax.text(x_pos_percentage, y_pos_percentage,
                f'{percentages[i]:.1f}%',
                ha='center',
                va='center',
                color='black',
                fontsize=9,
                fontweight='bold')

    ax.set_title("Общая нагрузка", fontsize=16, fontweight='bold')
    ax.axis('equal')
    plt.savefig('/app/data_output/charts_summary.png', dpi=300)