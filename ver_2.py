import re

data_dict = {"2": {"key": "1", "qwer": "1", "raw": 0, "column": 1},
             "3": {"key": "2", "qwer": "2", "raw": 0, "column": 2},
             "4": {"key": "3", "qwer": "3", "raw": 0, "column": 3},
             "5": {"key": "4", "qwer": "4", "raw": 0, "column": 4},
             "6": {"key": "5", "qwer": "5", "raw": 0, "column": 5},
             "7": {"key": "6", "qwer": "6", "raw": 0, "column": 6},
             "8": {"key": "7", "qwer": "7", "raw": 0, "column": 7},
             "9": {"key": "8", "qwer": "8", "raw": 0, "column": 8},
             "10": {"key": "9", "qwer": "9", "raw": 0, "column": 9},
             "11": {"key": "0", "qwer": "0", "raw": 0, "column": 10},
             "12": {"key": "*", "qwer": "-", "raw": 0, "column": 11},
             "13": {"key": "=", "qwer": "=", "raw": 0, "column": 12},
             "14": {"key": "ъ", "qwer": "", "raw": 0, "column": 0},
             "15": {"key": " ", "qwer": "", "raw": 0, "column": 0},
             "16": {"key": "ц", "qwer": "й", "raw": 1, "column": 1},
             "17": {"key": "ь", "qwer": "ц", "raw": 1, "column": 2},
             "18": {"key": "я", "qwer": "у", "raw": 1, "column": 3},
             "19": {"key": ",", "qwer": "к", "raw": 1, "column": 4},
             "20": {"key": ".", "qwer": "е", "raw": 1, "column": 5},
             "21": {"key": "з", "qwer": "н", "raw": 1, "column": 6},
             "22": {"key": "в", "qwer": "г", "raw": 1, "column": 7},
             "23": {"key": "к", "qwer": "ш", "raw": 1, "column": 8},
             "24": {"key": "д", "qwer": "щ", "raw": 1, "column": 9},
             "25": {"key": "ч", "qwer": "з", "raw": 1, "column": 10},
             "26": {"key": "ш", "qwer": "х", "raw": 1, "column": 11},
             "27": {"key": "щ", "qwer": "ъ", "raw": 1, "column": 12},
             "28": {"key": "", "qwer": "", "raw": 0, "column": 0},
             "29": {"key": "", "qwer": ",", "raw": 0, "column": 0},
             "30": {"key": "у", "qwer": "ф", "raw": 2, "column": 1},
             "31": {"key": "и", "qwer": "ы", "raw": 2, "column": 2},
             "32": {"key": "е", "qwer": "в", "raw": 2, "column": 3},
             "33": {"key": "о", "qwer": "а", "raw": 2, "column": 4},
             "34": {"key": "а", "qwer": "п", "raw": 2, "column": 5},
             "35": {"key": "л", "qwer": "р", "raw": 2, "column": 6},
             "36": {"key": "н", "qwer": "о", "raw": 2, "column": 7},
             "37": {"key": "т", "qwer": "л", "raw": 2, "column": 8},
             "38": {"key": "с", "qwer": "д", "raw": 2, "column": 9},
             "39": {"key": "р", "qwer": "ж", "raw": 2, "column": 10},
             "40": {"key": "й", "qwer": "э", "raw": 2, "column": 11},
             "41": {"key": "ё", "qwer": "ё", "raw": 0, "column": 0},
             "42": {"key": "", "qwer": "", "raw": 0, "column": 0},
             "43": {"key": "", "qwer": "", "raw": 0, "column": 0},
             "44": {"key": "ф", "qwer": "я", "raw": 3, "column": 1},
             "45": {"key": "э", "qwer": "ч", "raw": 3, "column": 2},
             "46": {"key": "х", "qwer": "с", "raw": 3, "column": 3},
             "47": {"key": "ы", "qwer": "м", "raw": 3, "column": 4},
             "48": {"key": "ю", "qwer": "и", "raw": 3, "column": 5},
             "49": {"key": "б", "qwer": "т", "raw": 3, "column": 6},
             "50": {"key": "м", "qwer": "ь", "raw": 3, "column": 7},
             "51": {"key": "п", "qwer": "б", "raw": 3, "column": 8},
             "52": {"key": "г", "qwer": "ю", "raw": 3, "column": 9},
             "53": {"key": "ж", "qwer": ".", "raw": 3, "column": 10},
             "54": {"key": "", "qwer": "", "raw": 3, "column": 10},
             "55": {"key": "", "qwer": "", "raw": 0, "column": 0},
             "56": {"key": "", "qwer": "", "raw": 0, "column": 0},
             "57": {"key": " ", "qwer": " ", "raw": 0, "column": 0},
             "58": {"key": "", "qwer": "", "raw": 0, "column": 0}}

counter_fingers = {'f5l': 0, 'f4l': 0, 'f3l': 0, 'f2l': 0, 'f1l': 0, 'f1r': 0, 'f2r': 0, 'f3r': 0, 'f4r': 0, 'f5r': 0}
counter_fingers_qwer = {'f5l': 0, 'f4l': 0, 'f3l': 0, 'f2l': 0, 'f1l': 0, 'f1r': 0, 'f2r': 0, 'f3r': 0, 'f4r': 0, 'f5r': 0}

def get_cords(symbol):
    """Получаем координаты символа для раскладки Диктор"""
    for key in data_dict:
        for value in data_dict[key]['key']:
            if value == symbol:
                return [data_dict[key]['raw'], data_dict[key]['column']]
    return None

def get_cords_qwer(symbol):
    """Получаем координаты символа для раскладки ЙЦУКЕН"""
    for key in data_dict:
        for value in data_dict[key]['qwer']:
            if value == symbol:
                return [data_dict[key]['raw'], data_dict[key]['column']]
    return None

def calculate_penalty(current_pos, next_pos):
    """
    Усовершенствованная система штрафных баллов согласно требованиям:
    - Вверх/вниз/влево/вправо = 1 балл
    - Диагональ = 2 балла
    - Сложные перемещения = 3-4 балла
    """
    if not current_pos or not next_pos:
        return 0
        
    current_row, current_col = current_pos
    next_row, next_col = next_pos
    
    # Если та же клавиша - штраф 0
    if current_row == next_row and current_col == next_col:
        return 0
    
    row_diff = abs(current_row - next_row)
    col_diff = abs(current_col - next_col)
    
    # Простые перемещения (1 балл)
    if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1):
        return 1
    
    # Диагональные перемещения (2 балла)
    elif row_diff == 1 and col_diff == 1:
        return 2
    
    # Сложные перемещения (3-4 балла)
    elif row_diff >= 2 or col_diff >= 2:
        base_penalty = row_diff + col_diff
        if next_col in [0, 12] or next_row == 0:
            base_penalty += 1
        return min(base_penalty, 4)
    
    else:
        return 1

def value_passing_fingers(column, value):
    """Распределение нагрузки по пальцам для Диктор"""
    match column:
        case 0 | 1:
            counter_fingers['f5l'] += value
        case 2:
            counter_fingers['f4l'] += value
        case 3:
            counter_fingers['f3l'] += value
        case 4 | 5:
            counter_fingers['f2l'] += value
        case 6 | 7:
            counter_fingers['f2r'] += value
        case 8:
            counter_fingers['f3r'] += value
        case 9:
            counter_fingers['f4r'] += value
        case 10 | 11 | 12:
            counter_fingers['f5r'] += value

def value_passing_fingers_qwer(column, value):
    """Распределение нагрузки по пальцам для ЙЦУКЕН"""
    match column:
        case 0 | 1:
            counter_fingers_qwer['f5l'] += value
        case 2:
            counter_fingers_qwer['f4l'] += value
        case 3:
            counter_fingers_qwer['f3l'] += value
        case 4 | 5:
            counter_fingers_qwer['f2l'] += value
        case 6 | 7:
            counter_fingers_qwer['f2r'] += value
        case 8:
            counter_fingers_qwer['f3r'] += value
        case 9:
            counter_fingers_qwer['f4r'] += value
        case 10 | 11 | 12:
            counter_fingers_qwer['f5r'] += value

def count_steps(first_sim, second_sim):
    """Подсчет шагов для раскладки Диктор с улучшенной системой штрафов"""
    current_pos = get_cords(first_sim)
    next_pos = get_cords(second_sim)
    
    if not current_pos or not next_pos:
        return 0, 'N/A'
    
    # Используем новую систему штрафов
    penalty = calculate_penalty(current_pos, next_pos)
    
    # Сохраняем оригинальную логику распределения
    if current_pos[1] == next_pos[1]:
        value_passing_fingers(next_pos[1], penalty)
    else:
        if current_pos[0] != next_pos[0]:
            match next_pos[1]:
                case 5 | 6:
                    if next_pos[0] == 2:
                        value_passing_fingers(next_pos[1], 1)
                    else:
                        value_passing_fingers(next_pos[1], penalty)
                case 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10:
                    if next_pos[0] == 2:
                        pass
                    else:
                        value_passing_fingers(next_pos[1], penalty)
                case 11:
                    value_passing_fingers(next_pos[1], penalty)
                case 12:
                    value_passing_fingers(next_pos[1], penalty)
        if current_pos[0] == next_pos[0]:
            match next_pos[1]:
                case 5 | 6 | 11:
                    value_passing_fingers(next_pos[1], abs(next_pos[0] - 2) + 1)
                case 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10:
                    value_passing_fingers(next_pos[1], abs(next_pos[0] - 2))
                case 12:
                    value_passing_fingers(next_pos[1], abs(next_pos[0] - 2) + 2)
    
    return penalty, get_finger_by_column(next_pos[1])

def count_steps_qwer(first_sim, second_sim):
    """Подсчет шагов для раскладки ЙЦУКЕН с улучшенной системой штрафов"""
    current_pos = get_cords_qwer(first_sim)
    next_pos = get_cords_qwer(second_sim)
    
    if not current_pos or not next_pos:
        return 0, 'N/A'
    
    penalty = calculate_penalty(current_pos, next_pos)
    
    if current_pos[1] == next_pos[1]:
        value_passing_fingers_qwer(next_pos[1], penalty)
    else:
        if current_pos[0] != next_pos[0]:
            match next_pos[1]:
                case 5 | 6:
                    if next_pos[0] == 2:
                        value_passing_fingers_qwer(next_pos[1], 1)
                    else:
                        value_passing_fingers_qwer(next_pos[1], penalty)
                case 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10:
                    if next_pos[0] == 2:
                        pass
                    else:
                        value_passing_fingers_qwer(next_pos[1], penalty)
                case 11:
                    value_passing_fingers_qwer(next_pos[1], penalty)
                case 12:
                    value_passing_fingers_qwer(next_pos[1], penalty)
        if current_pos[0] == next_pos[0]:
            match next_pos[1]:
                case 5 | 6 | 11:
                    value_passing_fingers_qwer(next_pos[1], abs(next_pos[0] - 2) + 1)
                case 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10:
                    value_passing_fingers_qwer(next_pos[1], abs(next_pos[0] - 2))
                case 12:
                    value_passing_fingers_qwer(next_pos[1], abs(next_pos[0] - 2) + 2)
    
    return penalty, get_finger_by_column(next_pos[1])

def get_finger_by_column(column):
    """Определяет палец по колонке"""
    match column:
        case 0 | 1:
            return 'f5l'
        case 2:
            return 'f4l'
        case 3:
            return 'f3l'
        case 4 | 5:
            return 'f2l'
        case 6 | 7:
            return 'f2r'
        case 8:
            return 'f3r'
        case 9:
            return 'f4r'
        case 10 | 11 | 12:
            return 'f5r'
        case _:
            return 'f1l'

def count_spaces(text):
    """Подсчет пробелов"""
    spaces = text.count(' ')
    counter_fingers_qwer['f1l'] += int(spaces * 0.6)
    counter_fingers_qwer['f1r'] += int(spaces * 0.4)
    counter_fingers['f1l'] += int(spaces * 0.55)
    counter_fingers['f1r'] += int(spaces * 0.45)

def analyze_movement_details(text):
    """Детальный анализ перемещений для отладки"""
    movements_info = []
    text_chars = [char for char in text.lower() if char.isalpha() or char in ' ,.']
    
    for i in range(1, min(50, len(text_chars))):  # Анализируем первые 50 перемещений
        current_char = text_chars[i-1]
        next_char = text_chars[i]
        
        # Для раскладки Диктор
        current_pos_d = get_cords(current_char)
        next_pos_d = get_cords(next_char)
        penalty_d, finger_d = count_steps(current_char, next_char)
        
        # Для раскладки ЙЦУКЕН (используем копию счетчиков чтобы не дублировать)
        current_pos_q = get_cords_qwer(current_char)
        next_pos_q = get_cords_qwer(next_char)
        penalty_q, finger_q = count_steps_qwer(current_char, next_char)
        
        # Определяем тип перемещения
        move_type_d = get_movement_type(current_pos_d, next_pos_d) if current_pos_d and next_pos_d else "N/A"
        move_type_q = get_movement_type(current_pos_q, next_pos_q) if current_pos_q and next_pos_q else "N/A"
        
        movements_info.append({
            'from': current_char,
            'to': next_char,
            'penalty_diktor': penalty_d,
            'penalty_qwer': penalty_q,
            'finger_diktor': finger_d,
            'finger_qwer': finger_q,
            'move_type_diktor': move_type_d,
            'move_type_qwer': move_type_q,
            'pos_diktor': f"({current_pos_d[0]},{current_pos_d[1]})→({next_pos_d[0]},{next_pos_d[1]})" if current_pos_d and next_pos_d else "N/A",
            'pos_qwer': f"({current_pos_q[0]},{current_pos_q[1]})→({next_pos_q[0]},{next_pos_q[1]})" if current_pos_q and next_pos_q else "N/A"
        })
    
    return movements_info

def get_movement_type(current_pos, next_pos):
    """Определяет тип перемещения"""
    if not current_pos or not next_pos:
        return "N/A"
    
    row_diff = abs(current_pos[0] - next_pos[0])
    col_diff = abs(current_pos[1] - next_pos[1])
    
    if row_diff == 0 and col_diff == 0:
        return "Та же клавиша"
    elif row_diff == 1 and col_diff == 0:
        return "Вертикаль (1)"
    elif row_diff == 0 and col_diff == 1:
        return "Горизонталь (1)"
    elif row_diff == 1 and col_diff == 1:
        return "Диагональ (2)"
    elif row_diff >= 2 or col_diff >= 2:
        return f"Сложное ({min(row_diff + col_diff, 4)})"
    else:
        return "Простое (1)"

def print_detailed_analysis(movements_info):
    """Печать детального анализа перемещений"""
    print("\n" + "="*120)
    print("ДЕТАЛЬНЫЙ АНАЛИЗ ПЕРЕМЕЩЕНИЙ (первые 20 перемещений)")
    print("="*120)
    print(f"{'Переход':^10} | {'Координаты (Д)':^20} | {'Тип (Д)':^12} | {'Штраф (Д)':^9} | {'Палец (Д)':^9} | "
          f"{'Координаты (Й)':^20} | {'Тип (Й)':^12} | {'Штраф (Й)':^9} | {'Палец (Й)':^9}")
    print("-"*120)
    
    for move in movements_info[:20]:
        print(f"{move['from']}→{move['to']:^7} | {move['pos_diktor']:^20} | {move['move_type_diktor']:^12} | "
              f"{move['penalty_diktor']:^9} | {move['finger_diktor']:^9} | "
              f"{move['pos_qwer']:^20} | {move['move_type_qwer']:^12} | "
              f"{move['penalty_qwer']:^9} | {move['finger_qwer']:^9}")

def print_movement_statistics(movements_info):
    """Статистика по типам перемещений"""
    print("\n" + "="*80)
    print("СТАТИСТИКА ТИПОВ ПЕРЕМЕЩЕНИЙ")
    print("="*80)
    
    stats_diktor = {}
    stats_qwer = {}
    
    for move in movements_info:
        type_d = move['move_type_diktor']
        type_q = move['move_type_qwer']
        
        stats_diktor[type_d] = stats_diktor.get(type_d, 0) + 1
        stats_qwer[type_q] = stats_qwer.get(type_q, 0) + 1
    
    print(f"{'Тип перемещения':<20} | {'Диктор':<8} | {'ЙЦУКЕН':<8}")
    print("-" * 50)
    all_types = set(list(stats_diktor.keys()) + list(stats_qwer.keys()))
    for move_type in sorted(all_types):
        count_d = stats_diktor.get(move_type, 0)
        count_q = stats_qwer.get(move_type, 0)
        print(f"{move_type:<20} | {count_d:<8} | {count_q:<8}")

def print_final_results():
    """Печать финальных результатов"""
    print("\n" + "="*80)
    print("ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ НАГРУЗКИ НА ПАЛЬЦЫ")
    print("="*80)
    
    print(f'\n{"":<15} | {"ДИКТОР":<15} | {"ЙЦУКЕН":<15} | {"Разница":<10}')
    print("-" * 60)
    
    fingers = ['f1l', 'f1r', 'f2l', 'f2r', 'f3l', 'f3r', 'f4l', 'f4r', 'f5l', 'f5r']
    finger_names = {
        'f1l': 'Большой лев', 'f1r': 'Большой прав',
        'f2l': 'Указ. лев', 'f2r': 'Указ. прав', 
        'f3l': 'Средний лев', 'f3r': 'Средний прав',
        'f4l': 'Безым. лев', 'f4r': 'Безым. прав',
        'f5l': 'Мизинец лев', 'f5r': 'Мизинец прав'
    }
    
    for finger in fingers:
        diktor_val = counter_fingers[finger]
        qwer_val = counter_fingers_qwer[finger]
        difference = diktor_val - qwer_val
        diff_sign = "+" if difference > 0 else ""
        
        print(f"{finger_names[finger]:<15} | {diktor_val:<15} | {qwer_val:<15} | {diff_sign}{difference:<9}")
    
    total_diktor = sum(counter_fingers.values())
    total_qwer = sum(counter_fingers_qwer.values())
    total_diff = total_diktor - total_qwer
    diff_sign = "+" if total_diff > 0 else ""
    
    print("-" * 60)
    print(f"{'ОБЩАЯ НАГРУЗКА':<15} | {total_diktor:<15} | {total_qwer:<15} | {diff_sign}{total_diff:<9}")
    print(f"{'Эффективность':<15} | {'Лучше' if total_diktor < total_qwer else 'Хуже':<15} | "
          f"{'Лучше' if total_qwer < total_diktor else 'Хуже':<15} | "
          f"{'Диктор' if total_diktor < total_qwer else 'ЙЦУКЕН':<9}")

if __name__ == "__main__":
    with open('voina-i-mir.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Обработка текста
    count_spaces(text)
    text = re.sub(r'[^А-Яа-яёЁ1-9,0\s]', '', text)
    text_list = list(text)
    
    # Учет заглавных букв
    list_upper_case = [i for i in text_list if i.isupper()]
    value_passing_fingers(0, len(list_upper_case) * 2)
    value_passing_fingers_qwer(0, len(list_upper_case) * 2)
    
    text_clean = ''.join(text_list)
    text_lower = [i.lower() for i in text_clean]
    
    # Детальный анализ (до основного подсчета)
    movements_info = analyze_movement_details(text_clean)
    
    # Основной анализ
    for i in range(1, len(text_lower)):
        count_steps(text_lower[i - 1], text_lower[i])
        count_steps_qwer(text_lower[i - 1], text_lower[i])
    
    # Вывод результатов
    print_detailed_analysis(movements_info)
    print_movement_statistics(movements_info)
    print_final_results()