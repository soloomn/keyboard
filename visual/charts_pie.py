import matplotlib.pyplot as plt
import numpy as np

def create_and_plot_pie_charts_group(data_diktor: dict,
                                     data_qwer: dict,
                                     data_vyzov: dict) -> None:
    """
    Строит 3 круговых диаграммы (по одной на раскладку),
    показывающих распределение нагрузки между левой и правой рукой.
    Args:
        data_diktor (dict): Данные для раскладки "Диктор".
        data_qwer (dict): Данные для раскладки "Йцукен".
        data_vyzov (dict): Данные для раскладки "Вызов".
        :rtype: None
    """
    layouts = {
        "ДИКТОР": data_diktor,
        "ЙЦУКЕН": data_qwer,
        "ВЫЗОВ": data_vyzov
    }

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    colors = ['#1f77b4', '#ff7f0e']
    labels = ['Левая рука', 'Правая рука']

    for i, (title, data) in enumerate(layouts.items()):
        # защита от пустых данных
        total = sum(data["left"]) + sum(data["right"])
        if total == 0 or np.isnan(total):
            axes[i].text(0.5, 0.5, "Нет данных", ha="center", va="center")
            axes[i].set_title(title)
            axes[i].axis("off")
            continue

        values = [sum(data['left']), sum(data['right'])]
        # Построение круговой диаграммы с использованием встроенных функций
        wedges, texts, autotexts = axes[i].pie(
            values,
            labels=labels,  # Отображаем основные метки ("Л. Рука", "П. Рука")
            colors=colors,
            autopct='%.1f%%',  # Включаем отображение процентов внутри сегментов
            pctdistance=0.6,  # Размещаем проценты ближе к центру (0.0 - центр, 1.0 - край)
            startangle=90,
            textprops = {'fontsize': 10}  # Стиль для основных меток (labels)
        )
        for text in autotexts:
            text.set_color('white')
            text.set_fontweight('bold')

        axes[i].set_title(title, fontsize=12, fontweight='bold')
        axes[i].axis('equal')

    plt.suptitle("Сравнение нагрузок на руки по раскладкам", fontsize=16, fontweight='bold')  # Общий заголовок
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Автоматически настраивает расположение подграфиков
    plt.savefig('/app/data_output/charts_pie.png', dpi=300)