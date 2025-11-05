"""
Модуль для построения множественных графиков сравнения нагрузок на пальцы.

Содержит функцию plot_finger_loads_by_layout для визуализации распределения нагрузок
по типам пальцев (большой, указательный, средний, безымянный, мизинец)
сравнивая семь различных клавиатурных раскладок.

Основные возможности:
- Создание 5 отдельных графиков (по одному на каждый тип пальца)
- Сравнение нагрузок для левой и правой руки на каждом графике
- Визуализация данных для 7 различных раскладок клавиатуры
- Автоматическое сохранение результата в файл

Используемые библиотеки:
- matplotlib для построения графиков
- pandas для работы с данными в табличном формате
"""

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def plot_finger_loads_by_layout(data_diktor: dict,
                                data_qwer: dict,
                                data_vyzov: dict,
                                data_ant: dict,
                                data_skoropis: dict,
                                data_zubachew: dict,
                                data_rusphone: dict) -> None:
    """
    Строит 5 отдельных графиков — нагрузку на каждый тип пальца по семи раскладкам.

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
        - Создает 5 графиков (2x3 сетка) - по одному на каждый тип пальца
        - На каждом графике отображает нагрузки для левой (Л) и правой (П) руки
        - Сравнивает 7 раскладок клавиатуры разными цветами
        - Сохраняет все графики в файл '/app/data_output/charts_multi.png' с разрешением 300 DPI
        - Добавляет легенду с названиями раскладок на каждом графике
        - Настраивает заголовки и подписи осей для каждого типа пальца
    """
    finger_types = ['Большой', 'Указательный', 'Средний', 'Безымянный', 'Мизинец']

    # Функция для преобразования данных в DataFrame
    def prepare_data(data: dict, layout_name: str) -> DataFrame:
        """
        Преобразует данные раскладки в DataFrame для построения графиков.

        ВХОД:
            data (dict): Данные раскладки в формате {'left': list, 'right': list}
            layout_name (str): Название раскладки

        ВЫХОД:
            DataFrame: Таблица с колонками ['Палец', 'Нагрузка', 'Раскладка']
        """
        rows = []
        for i, ftype in enumerate(finger_types):
            rows.append({'Палец': f"{ftype} Л", 'Нагрузка': data['left'][i], 'Раскладка': layout_name})
            rows.append({'Палец': f"{ftype} П", 'Нагрузка': data['right'][i], 'Раскладка': layout_name})
        return pd.DataFrame(rows)

    df_all = pd.concat([
        prepare_data(data_diktor, 'Диктор'),
        prepare_data(data_qwer, 'Йцукен'),
        prepare_data(data_vyzov, 'Вызов'),
        prepare_data(data_ant, 'Ант'),
        prepare_data(data_skoropis, 'Скоропись'),
        prepare_data(data_zubachew, 'Зубачёв'),
        prepare_data(data_rusphone, 'РусФон')
    ])

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    colors = {"Йцукен": "#FF0000", "Диктор": "#FBFF00", "Вызов": "#000000",
              "Ант": "#0000FF", "Скоропись": "#008000", "Зубачев": "#9467bd", "РусФон": "#FFC0CB"}

    for i, ftype in enumerate(finger_types):
        ax = axes[i]
        sub = df_all[df_all['Палец'].str.startswith(ftype)]
        for layout, color in colors.items():
            d = sub[sub['Раскладка'] == layout]
            ax.plot(d['Палец'], d['Нагрузка'], marker='o', label=layout, color=color)
        ax.set_title(ftype)
        ax.set_ylabel('Нагрузка (количество нажатий)')
        ax.ticklabel_format(style='plain', axis='y')  # Отключить научную нотацию для оси Y
        ax.tick_params(axis='x', rotation=45)
        ax.legend()

    for j in range(len(finger_types), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig('/app/data_output/charts_multi.png', dpi=300 )