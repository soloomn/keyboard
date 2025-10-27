import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def plot_finger_loads_by_layout(data_diktor: dict,
                                data_qwer: dict,
                                data_vyzov: dict) -> None:
    """
    Строит 5 отдельных графиков — нагрузку на каждый тип пальца
    (большой, указательный, средний, безымянный, мизинец)
    по трем раскладкам.

    Args:
        data_diktor (dict): Данные для раскладки "Диктор".
        data_qwer (dict): Данные для раскладки "Йцукен".
        data_vyzov (dict): Данные для раскладки "Вызов".
        :rtype: None
    """
    finger_types = ['Большой', 'Указательный', 'Средний', 'Безымянный', 'Мизинец']

    # Функция для преобразования данных в DataFrame
    def prepare_data(data: dict, layout_name: str) -> DataFrame:
        """
        Преобразует данные раскладки в DataFrame, где каждая строка - это нагрузка
        для конкретного пальца (Левый/Правый) в данной раскладке.
        :rtype: DataFrame
        :param data:
        :param layout_name:
        """
        rows = []
        for i, ftype in enumerate(finger_types):
            rows.append({'Палец': f"{ftype} Л", 'Нагрузка': data['left'][i], 'Раскладка': layout_name})
            rows.append({'Палец': f"{ftype} П", 'Нагрузка': data['right'][i], 'Раскладка': layout_name})
        return pd.DataFrame(rows)

    df_all = pd.concat([
        prepare_data(data_diktor, 'Диктор'),
        prepare_data(data_qwer, 'Йцукен'),
        prepare_data(data_vyzov, 'Вызов')
    ])

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    colors = {"Йцукен": "#FF0000", "Диктор": "#FBFF00", "Вызов": "#000000"}

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