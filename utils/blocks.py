"""
Модуль для обработки текстовых блоков и объединения данных анализа.

Содержит функции для параллельной обработки текстовых блоков
и последующего объединения результатов анализа раскладок.
"""

from models import LayoutAnalyzer

def process_block_return(block_text: str) -> dict:
    """
    Обрабатывает блок текста и возвращает промежуточные данные для всех раскладок.

    ВХОД:
        block_text (str): Текстовый блок для анализа

    ВЫХОД:
        dict: Словарь с данными нагрузки для всех раскладок в формате reverser
    """
    analyzer = LayoutAnalyzer()
    analyzer.analyze_text(block_text)
    analyzer.analyze_sequences(block_text)

    finger_data = analyzer.reverser
    sequence_stats = analyzer.stats_reverser

    result = {
        'finger_data': finger_data,
        'sequence_stats': sequence_stats
    }

    return result

def merge_block_data(main_analyzer: LayoutAnalyzer, block_data: dict):
    """
    Добавляет данные из блока в основной LayoutAnalyzer.

    ВХОД:
        main_analyzer (LayoutAnalyzer): Основной анализатор для накопления данных
        block_data (dict): Данные из блока для объединения

    ВЫХОД: Нет (данные добавляются в основной анализатор)
    """
    for layout_name, vals in block_data['finger_data'].items():
        layout = main_analyzer.layouts[layout_name]

        # Суммируем нагрузку по пальцам
        layout.counter_fingers['f1l'] += vals['left'][0]
        layout.counter_fingers['f2l'] += vals['left'][1]
        layout.counter_fingers['f3l'] += vals['left'][2]
        layout.counter_fingers['f4l'] += vals['left'][3]
        layout.counter_fingers['f5l'] += vals['left'][4]

        layout.counter_fingers['f1r'] += vals['right'][0]
        layout.counter_fingers['f2r'] += vals['right'][1]
        layout.counter_fingers['f3r'] += vals['right'][2]
        layout.counter_fingers['f4r'] += vals['right'][3]
        layout.counter_fingers['f5r'] += vals['right'][4]

        layout.hand_changes += vals['two_handed']

        layout.key_presses['f1l'] += vals['left_press'][0]
        layout.key_presses['f2l'] += vals['left_press'][1]
        layout.key_presses['f3l'] += vals['left_press'][2]
        layout.key_presses['f4l'] += vals['left_press'][3]
        layout.key_presses['f5l'] += vals['left_press'][4]

        layout.key_presses['f1r'] += vals['right_press'][0]
        layout.key_presses['f2r'] += vals['right_press'][1]
        layout.key_presses['f3r'] += vals['right_press'][2]
        layout.key_presses['f4r'] += vals['right_press'][3]
        layout.key_presses['f5r'] += vals['right_press'][4]

    for layout_name, stats in block_data["sequence_stats"].items():
        layout = main_analyzer.layouts[layout_name]

        layout.twogram["udp_2gram"] += stats["udp_2gram"]
        layout.twogram["chudp_2gram"] += stats["chudp_2gram"]
        layout.twogram["nudp_2gram"] += stats["nudp_2gram"]

        layout.threegram["udp_3gram"] += stats["udp_3gram"]
        layout.threegram["chudp_3gram"] += stats["chudp_3gram"]
        layout.threegram["nudp_3gram"] += stats["nudp_3gram"]

        layout.fourgram["udp_4gram"] += stats["udp_4gram"]
        layout.fourgram["chudp_4gram"] += stats["chudp_4gram"]
        layout.fourgram["nudp_4gram"] += stats["nudp_4gram"]

        layout.total_sequences += stats["total_sequences"]