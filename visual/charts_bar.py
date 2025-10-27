import matplotlib.pyplot as plt
import numpy as np
from matplotlib.container import BarContainer


def plot_finger_usage_with_values(data_diktor: dict,
                                  data_qwer: dict,
                                  data_vyzov: dict) -> None:
    """
    Строит горизонтальную гистограмму нагрузок по пальцам
    для трёх раскладок: Йцукен, Диктор и Вызов.

    Args:
        data_diktor (dict): Данные для раскладки "Диктор".
        data_qwer (dict): Данные для раскладки "Йцукен".
        data_vyzov (dict): Данные для раскладки "Вызов".
        :rtype: None
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

    # Цвета для раскладок
    colors = {
        "Йцукен": "#FF0000",  # Красный для Йцукен
        "Диктор": "#FBFF00",  # Жёлтый для Диктор
        "Вызов": "#000000"  # Чёрный для Вызов
    }

    # Позиции столбцов на оси Y
    index = np.arange(len(fingers))

    # Ширина столбцов. Сделаем ее немного меньше, чтобы было место для текста.
    bar_width = 0.2

    # Построение горизонтальной гистограммы
    # plt.barh возвращает список объектов `Rectangle` (прямоугольники, т.е. столбцы)
    fig, ax = plt.subplots(figsize=(12, 8))
    rects1 = ax.barh(index - bar_width, layout_qwer, bar_width, label='Йцукен', color=colors['Йцукен'])
    rects2 = ax.barh(index, layout_diktor, bar_width, label='Диктор', color=colors['Диктор'])
    rects3 = ax.barh(index + bar_width, layout_vyzov, bar_width, label='Вызов', color=colors['Вызов'])

    # Добавление значений (текста) справа от столбцов
    # Проходимся по каждому объекту столбика и добавляем текст

    # Функция для добавления текста к столбцам.
    # Это более удобный способ, чем повторять код для каждого набора столбцов.
    def add_labels(rects: BarContainer, ax, x_offset: object = 80) -> None:
        """Добавляет текстовые метки значений справа от столбцов.
        :rtype: None
        :param rects:
        :param ax:
        :param x_offset:
        """
        for rect in rects:
            # Получаем ширину столбца (т.е. его значение)
            width = rect.get_width()
            # Получаем Y-координату центра столбца
            y_pos = rect.get_y() + rect.get_height() / 2

            # Добавляем текстовую метку.
            # x_pos = width + x_offset: Позиция X - это конец столбца плюс небольшой отступ.
            # y_pos: Центр столбца по оси Y.
            # text='{}'.format(width): Сам текст метки - это значение столбца.
            # va='center': Вертикальное выравнивание по центру.
            # ha='left': Горизонтальное выравнивание - начало текста слева от x_pos.
            ax.text(width + x_offset, y_pos, f'{width:.0f}', va='center', ha='left', fontsize=9)

    # Добавляем метки для каждого набора столбцов
    add_labels(rects1, ax, x_offset=80)  # Смещение 80 пикселей
    add_labels(rects2, ax, x_offset=80)
    add_labels(rects3, ax, x_offset=80)

    # Добавление подписей и заголовков
    ax.set_ylabel('Пальцы')
    ax.set_xlabel('Нагрузки (количество нажатий)')
    ax.set_title('Сравнение нагрузок на пальцы в раскладках йцукен, диктор и вызов')
    ax.set_yticks(index, fingers)  # Устанавливаем метки для оси Y

    # Добавляем небольшой отступ справа, чтобы значения не обрезались
    # ax.margins(x=0.1) # Этот метод может сработать, но лучше установить лимит оси вручную

    # Устанавливаем лимит правой оси X, чтобы текст значений помещался
    # Находим максимальное значение среди всех раскладок
    max_value = max(max(layout_vyzov), max(layout_diktor), max(layout_qwer))
    # Устанавливаем правый лимит оси X чуть больше максимального значения + отступ
    ax.set_xlim(0, max_value * 1.2)  # 1.15 - это 15% от максимального значения как запас

    # Легенда
    ax.legend()

    # Показ гистограммы
    plt.tight_layout()  # Автоматически корректирует параметры графика для плотного расположения
    plt.savefig('/app/data_output/charts_bar.png', dpi=300)