from models import LayoutAnalyzer

def process_block_return(block_text: str) -> dict:
    """
    Обрабатывает блок текста и возвращает промежуточные данные для всех раскладок.
    """
    analyzer = LayoutAnalyzer()
    analyzer.analyze_text(block_text)
    return analyzer.reverser  # словарь с нагрузкой для всех раскладок

def merge_block_data(main_analyzer: LayoutAnalyzer, block_data: dict):
    """
    Добавляет данные из блока в основной LayoutAnalyzer.
    """
    for layout_name, vals in block_data.items():
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

        # Суммируем переходы между руками
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
