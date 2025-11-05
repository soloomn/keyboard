"""
Модуль для построения круговых диаграмм распределения нагрузок на руки.

Содержит функции для визуализации соотношения нагрузок между левой и правой рукой
для различных клавиатурных раскладок в виде набора круговых диаграмм.

Основные возможности:
- Создание 7 круговых диаграмм (по одной для каждой раскладки)
- Визуализация распределения нагрузок: левая рука, правая рука, двуручие
- Отображение процентных значений внутри сегментов диаграмм
- Автоматическое выделение максимального сегмента (взрыв диаграммы)
- Сохранение результата в файл

Используемые библиотеки:
- matplotlib для построения графиков
- numpy для математических вычислений
"""

import matplotlib.pyplot as plt
import numpy as np

# --- Функция для создания одной круговой диаграммы (ОБНОВЛЕННАЯ) ---
def create_pie_chart(ax, values_left, values_right, values_two_handed,
                     labels_base, title, explode):  # labels_base - базовые метки
    """
    Создает одну круговую диаграмму на переданных осях (ax) с тремя секторами.

    ВХОД:
        ax (Axes): Объект осей matplotlib для отрисовки диаграммы
        values_left (float): Суммарная нагрузка на левую руку
        values_right (float): Суммарная нагрузка на правую руку
        values_two_handed (float): Суммарная нагрузка на двуручные операции
        labels_base (list): Базовые метки для сегментов ['Л. Рука', 'П. Рука', 'Двуручие']
        title (str): Заголовок диаграммы
        explode (tuple): Кортеж из 3 элементов для выделения сегментов (0-без выделения, >0-с выделением)

    ВЫХОД:
        Axes: Объект осей с построенной диаграммой

    Действия функции:
        - Создает круговую диаграмму с тремя сегментами
        - Рассчитывает процентное соотношение нагрузок
        - Добавляет процентные значения внутри каждого сегмента
        - Настраивает цвета и стиль отображения
    """
    color_left = "#1f77b4"  # Синий
    color_right = "#ff7f0e"  # Оранжевый
    color_two_handed = "#9467bd"  # Фиолетовый

    values = [values_left, values_right, values_two_handed]
    colors = [color_left, color_right, color_two_handed]

    total = sum(values)

    # Рассчитываем проценты
    if total == 0:
        percentages_float = [0.0, 0.0, 0.0]
    else:
        percentages_float = [(v / total) * 100 for v in values]

    # --- Отрисовка диаграммы ---
    # Теперь используем final_labels для меток.
    # Autopct будет отключен, так как проценты уже в метках.
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels_base,  # Используем финальные метки
        colors=colors,
        autopct='',  # Отключено
        pctdistance=0.7,  # Отступ для autotexts, если бы он был включен
        labeldistance=1.1,  # Расстояние от центра для меток
        startangle=90,
        explode=None,
        textprops={'fontsize': 8, 'color': 'black'}  # Стиль для обычных меток
    )

    # --- Добавление процентов для "Л. Рука" и "П. Рука" (внутри сегментов) ---
    # Поскольку процент "Двуручия" уже в названии, мы добавляем проценты только для рук.
    for i, wedge in enumerate(wedges):
        # Определяем позицию и цвет текста процента
        center_angle_rad = (wedge.theta1 + wedge.theta2) / 2
        percentage_radius = 0.55  # Ближе к центру
        percentage_color = 'white'  # Белый цвет
        percentage_fontsize = 10

        x_pos = percentage_radius * np.cos(np.deg2rad(center_angle_rad))
        y_pos = percentage_radius * np.sin(np.deg2rad(center_angle_rad))

        # Добавляем текст процента
        ax.text(x_pos, y_pos, f'{percentages_float[i]:.1f}%',
                ha='center', va='center',
                color=percentage_color,
                fontweight='bold',
                fontsize=percentage_fontsize)

    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.axis('equal')
    return ax


def plot_all_pie_charts(data_dictor, data_ytsuken, data_visov, data_ant, data_scoropis, data_zubachev, data_rusfon,
                        axes_list):
    """
    Рисует 7 круговых диаграмм на переданных осях `axes_list`.

    ВХОД:
        data_dictor (dict): Данные для раскладки "Диктор"
        data_ytsuken (dict): Данные для раскладки "Йцукен"
        data_visov (dict): Данные для раскладки "Вызов"
        data_ant (dict): Данные для раскладки "Ант"
        data_scoropis (dict): Данные для раскладки "Скоропись"
        data_zubachev (dict): Данные для раскладки "Зубачев"
        data_rusfon (dict): Данные для раскладки "РусФон"
        axes_list (list): Список из 7 объектов осей matplotlib для отрисовки диаграмм

    Структура данных для каждой раскладки:
        - 'left': список нагрузок для левой руки
        - 'right': список нагрузок для правой руки
        - 'two_handed': значение нагрузки на двуручные операции

    ВЫХОД:
        None

    Действия функции:
        - Обрабатывает данные для каждой из 7 раскладок
        - Автоматически выделяет максимальный сегмент на каждой диаграмме
        - Вызывает create_pie_chart для построения каждой отдельной диаграммы
    """
    # --- Данные и настройки для каждой раскладки ---
    pie_configs = [
        (data_ytsuken, "ЙЦУКЕН", axes_list[0]),
        (data_dictor, "Диктор", axes_list[1]),
        (data_visov, "Вызов", axes_list[2]),
        (data_ant, "Ант", axes_list[3]),
        (data_scoropis, "Скоропись", axes_list[4]),
        (data_zubachev, "Зубачев", axes_list[5]),
        (data_rusfon, "РусФон", axes_list[6])
    ]

    # --- Рисуем каждую круговую диаграмму ---
    for data, title_prefix, ax in pie_configs:

        # --- Получаем значения (предполагаем, что 'left', 'right', 'two_handed' есть) ---
        values_left = sum(data.get('left', [0]))
        values_right = sum(data.get('right', [0]))
        values_two_handed = data.get('two_handed', 0)

        labels_for_pie = ['Л. Рука', 'П. Рука', 'Двуручие']

        # Логика explode: выдвигаем сектор, который больше всех
        max_value = max(values_left, values_right, values_two_handed)
        explode = (0, 0, 0)
        if max_value == values_left and max_value != 0:
            explode = (0.08, 0, 0)
        elif max_value == values_right and max_value != 0:
            explode = (0, 0.08, 0)
        elif max_value == values_two_handed and max_value != 0:
            explode = (0, 0, 0.08)

        create_pie_chart(ax, values_left, values_right, values_two_handed,
                         labels_for_pie, title_prefix, explode)


# --- ОСНОВНАЯ ФУНКЦИЯ ДЛЯ ПОСТРОЕНИЯ ТОЛЬКО КРУГОВЫХ ДИАГРАММ ---
def plot_only_pie_charts(data_dictor, data_ytsuken, data_visov,
                         data_ant, data_scoropis, data_zubachev, data_rusfon):
    """
    Создает фигуру только с семью круговыми диаграммами.

    ВХОД:
        data_dictor (dict): Данные для раскладки "Диктор"
        data_ytsuken (dict): Данные для раскладки "Йцукен"
        data_visov (dict): Данные для раскладки "Вызов"
        data_ant (dict): Данные для раскладки "Ант"
        data_scoropis (dict): Данные для раскладки "Скоропись"
        data_zubachev (dict): Данные для раскладки "Зубачев"
        data_rusfon (dict): Данные для раскладки "РусФон"

    Структура данных для каждой раскладки:
        - 'left': список нагрузок для левой руки
        - 'right': список нагрузок для правой руки
        - 'two_handed': значение нагрузки на двуручные операции

    ВЫХОД:
        None

    Действия функции:
        - Создает сетку графиков 3x3 (9 осей)
        - Строит 7 круговых диаграмм на первых 7 осях
        - Удаляет 2 пустые оси
        - Добавляет общий заголовок
        - Сохраняет результат в файл '/app/data_output/charts_pie.png'
    """
    # --- Создание сетки графиков ---
    # Нам нужно 7 круговых диаграмм. Сетка 3x3 (9 осей) - оптимальный вариант.
    # Последние две оси останутся пустыми.
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 15))

    # Flatten axes. Получим 9 осей: [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
    axes = axes.flatten()

    # --- Размещение круговых диаграмм ---
    # Круговые диаграммы будут на осях с индексами 0, 1, 2, 3, 4, 5, 6.
    # Это первые 7 осей.
    axes_for_pies = axes[0:7]  # Берем оси с индексами 0, 1, 2, 3, 4, 5, 6

    # --- Рисуем круговые диаграммы ---
    plot_all_pie_charts(data_dictor, data_ytsuken, data_visov, data_ant, data_scoropis, data_zubachev, data_rusfon,
                        axes_for_pies)

    # --- Удаляем лишние, пустые оси ---
    # У нас 7 диаграмм, но 9 осей. Оси с индексами 7 и 8 останутся пустыми.
    fig.delaxes(axes[7])
    fig.delaxes(axes[8])

    # --- Общий заголовок ---
    plt.suptitle("Сравнение нагрузок на руки и двуручия по раскладкам", fontsize=18, fontweight='bold')

    # --- Автоматическое улучшение расположения элементов ---
    # `rect` оставляет место сверху для suptitle
    plt.tight_layout()
    plt.savefig('/app/data_output/charts_pie.png', dpi=300)