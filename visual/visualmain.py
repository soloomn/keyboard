import json
from visual import plot_finger_usage_with_values
from visual import create_and_plot_pie_charts_group
from visual import plot_finger_loads_by_layout
from visual import create_total_load_pie_chart


def show_all(data_diktor: dict, data_qwer: dict, data_vyzov: dict) -> None:
    """

    :rtype: None
    :param data_diktor:
    :param data_qwer:
    :param data_vyzov:
    """
    plot_finger_usage_with_values(data_diktor, data_qwer, data_vyzov)
    create_and_plot_pie_charts_group(data_diktor, data_qwer, data_vyzov)
    plot_finger_loads_by_layout(data_diktor, data_qwer, data_vyzov)
    create_total_load_pie_chart(data_diktor, data_qwer, data_vyzov)

# загружаем данные из JSON
with open("/app/data_output/layouts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

show_all(data['diktor'], data['qwer'], data['vyzov'])