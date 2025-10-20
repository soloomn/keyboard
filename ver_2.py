"""
МОДУЛЬ АНАЛИЗА ЭРГОНОМИКИ КЛАВИАТУРНЫХ РАСКЛАДОК
------------------------------------------------
ОПИСАНИЕ:
---------
Данный модуль предназначен для сравнительного анализа эргономичности трёх русских раскладок клавиатуры:
"Диктор" и "Вызов" (альтернативные раскладки) и "ЙЦУКЕН" (стандартная раскладка).

ОСНОВНЫЕ ВОЗМОЖНОСТИ:
---------------------
1. Расчет штрафных баллов за перемещения между клавишами
2. Распределение нагрузки на пальцы обеих рук
3. Сравнительный анализ эффективности раскладок
4. Детальная статистика по типам перемещений
5. Визуализация результатов в табличном формате

ПРИНЦИП РАБОТЫ:
---------------
- Текст разбивается на последовательности символов
- Для каждой пары символов вычисляются координаты в обеих раскладках
- На основе расстояния между координатами начисляются штрафные баллы
- Нагрузка распределяется по 10 пальцам согласно зонам ответственности
- Сравнивается общая нагрузка и эффективность раскладок

ВХОДНЫЕ ДАННЫЕ:
---------------
- Файл 'text.txt' с русским текстом для анализа
- Модуль dictr.py с конфигурацией клавиатурных раскладок (data_dict)

ВЫХОДНЫЕ ДАННЫЕ:
----------------
- Детальный анализ первых 20 перемещений между символами
- Статистика по типам перемещений (вертикальные, горизонтальные, диагональные, сложные)
- Сравнительная таблица нагрузки на каждый палец для обеих раскладок
- Общий вердикт по эффективности раскладок с итоговыми баллами

СИСТЕМА ШТРАФНЫХ БАЛЛОВ:
------------------------
- 0 баллов: та же клавиша
- 1 балл: вертикальные/горизонтальные перемещения на 1 позицию
- 2 балла: диагональные перемещения
- 3-4 балла: сложные перемещения (2+ позиции)

РАСПРЕДЕЛЕНИЕ ПАЛЬЦЕВ:
----------------------
- f1l/f1r: большие пальцы (пробелы и спец. клавиши)
- f2l/f2r: указательные пальцы
- f3l/f3r: средние пальцы
- f4l/f4r: безымянные пальцы
- f5l/f5r: мизинцы
"""
import re
from dictr import *

counter_fingers = {'f5l': 0, 'f4l': 0, 'f3l': 0, 'f2l': 0, 'f1l': 0, 'f1r': 0, 'f2r': 0, 'f3r': 0, 'f4r': 0, 'f5r': 0}
counter_fingers_qwer = {'f5l': 0, 'f4l': 0, 'f3l': 0, 'f2l': 0, 'f1l': 0, 'f1r': 0, 'f2r': 0, 'f3r': 0, 'f4r': 0, 'f5r': 0}
counter_fingers_call = {'f5l': 0, 'f4l': 0, 'f3l': 0, 'f2l': 0, 'f1l': 0, 'f1r': 0, 'f2r': 0, 'f3r': 0, 'f4r': 0, 'f5r': 0}


def get_cords(symbol):
    """
    Получаем координаты символа для раскладки Диктор

    ВХОД:
        symbol (str): символ для поиска координат

    ВЫХОД:
        list | None: [номер_ряда, номер_колонки] или None если символ не найден
    """
    for key in data_dict:
        for value in data_dict[key]['key']:
            if value == symbol:
                return [data_dict[key]['raw'], data_dict[key]['column']]
    return None


def get_cords_qwer(symbol):
    """
    Получаем координаты символа для раскладки ЙЦУКЕН

    ВХОД:
        symbol (str): символ для поиска координат

    ВЫХОД:
        list | None: [номер_ряда, номер_колонки] или None если символ не найден
    """
    for key in data_dict:
        for value in data_dict[key]['qwer']:
            if value == symbol:
                return [data_dict[key]['raw'], data_dict[key]['column']]
    return None


def get_cords_vyzov(symbol):
    """
    Получаем координаты символа для раскладки Вызов и определяем, является ли символ вторым на клавише

    ВХОД:
        symbol (str): символ для поиска координат

    ВЫХОД:
        list | None: [номер_ряда, номер_колонки] или None если символ не найден
    """
    for key in data_dict:
        vyzov_chars = data_dict[key]['vyzov'].strip()
        if len(vyzov_chars) == 2:
            # Клавиша с двумя символами
            if vyzov_chars[0] == symbol:
                return [data_dict[key]['raw'], data_dict[key]['column'], False]  # Первый символ
            elif vyzov_chars[1] == symbol:
                return [data_dict[key]['raw'], data_dict[key]['column'], True]  # Второй символ
        elif len(vyzov_chars) == 1:
            # Клавиша с одним символом
            if vyzov_chars[0] == symbol:
                return [data_dict[key]['raw'], data_dict[key]['column'], False]
    return None


def calculate_penalty(current_pos, next_pos):
    """
    Усовершенствованная система штрафных баллов согласно требованиям:
    - Вверх/вниз/влево/вправо = 1 балл
    - Диагональ = 2 балла
    - Сложные перемещения = 3-4 балла

    ВХОД:
        current_pos (list): текущие координаты [ряд, колонка]
        next_pos (list): следующие координаты [ряд, колонка]

    ВЫХОД:
        int: штрафные баллы (0-4)
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
    """
    Распределение нагрузки по пальцам для Диктор

    ВХОД:
        column (int): номер колонки (0-12)
        value (int): значение нагрузки для добавления

    ВЫХОД:
        None: обновляет глобальную переменную counter_fingers
    """
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
    """
    Распределение нагрузки по пальцам для ЙЦУКЕН

    ВХОД:
        column (int): номер колонки (0-12)
        value (int): значение нагрузки для добавления

    ВЫХОД:
        None: обновляет глобальную переменную counter_fingers_qwer
    """
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


def value_passing_fingers_call(column, value, is_second_symbol=False):
    """
    Распределение нагрузки по пальцам для Вызов

    ВХОД:
        column (int): номер колонки (0-12)
        value (int): значение нагрузки для добавления

    ВЫХОД:
        None: обновляет глобальную переменную counter_fingers_qwer
    """
    # Добавляем штраф за использование второго символа
    total_value = value + (4 if is_second_symbol else 0)

    match column:
        case 0 | 1:
            counter_fingers_call['f5l'] += total_value
        case 2:
            counter_fingers_call['f4l'] += total_value
        case 3:
            counter_fingers_call['f3l'] += total_value
        case 4 | 5:
            counter_fingers_call['f2l'] += total_value
        case 6 | 7:
            counter_fingers_call['f2r'] += total_value
        case 8:
            counter_fingers_call['f3r'] += total_value
        case 9:
            counter_fingers_call['f4r'] += total_value
        case 10 | 11 | 12:
            counter_fingers_call['f5r'] += total_value


def count_steps(first_sim, second_sim):
    """
    Подсчет шагов для раскладки Диктор с улучшенной системой штрафов

    ВХОД:
        first_sim (str): первый символ
        second_sim (str): второй символ

    ВЫХОД:
        tuple: (штрафные_баллы, используемый_палец)
    """
    current_pos = get_cords(first_sim)
    next_pos = get_cords(second_sim)

    if not current_pos or not next_pos:
        return 0, 'N/A'

    penalty = calculate_penalty(current_pos, next_pos)

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
    """
    Подсчет шагов для раскладки ЙЦУКЕН с улучшенной системой штрафов

    ВХОД:
        first_sim (str): первый символ
        second_sim (str): второй символ

    ВЫХОД:
        tuple: (штрафные_баллы, используемый_палец)
    """
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


def count_steps_call(first_sim, second_sim):
    """
    Подсчет шагов для раскладки Вызов с улучшенной системой штрафов

    ВХОД:
        first_sim (str): первый символ
        second_sim (str): второй символ

    ВЫХОД:
        tuple: (штрафные_баллы, используемый_палец)
    """
    current_pos_info = get_cords_vyzov(first_sim)
    next_pos_info = get_cords_vyzov(second_sim)

    if not current_pos_info or not next_pos_info:
        return 0, 'N/A'

    # Извлекаем координаты и информацию о втором символе
    current_pos = current_pos_info[:2]  # row, column
    next_pos = next_pos_info[:2]  # row, column
    is_second_symbol_current = current_pos_info[2] if len(current_pos_info) > 2 else False
    is_second_symbol_next = next_pos_info[2] if len(next_pos_info) > 2 else False

    penalty = calculate_penalty(current_pos, next_pos)

    # Учитываем штраф за второй символ только для конечной позиции
    if current_pos[1] == next_pos[1]:
        value_passing_fingers_call(next_pos[1], penalty, is_second_symbol_next)
    else:
        if current_pos[0] != next_pos[0]:
            match next_pos[1]:
                case 5 | 6:
                    if next_pos[0] == 2:
                        value_passing_fingers_call(next_pos[1], 1, is_second_symbol_next)
                    else:
                        value_passing_fingers_call(next_pos[1], penalty, is_second_symbol_next)
                case 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10:
                    if next_pos[0] == 2:
                        pass
                    else:
                        value_passing_fingers_call(next_pos[1], penalty, is_second_symbol_next)
                case 11:
                    value_passing_fingers_call(next_pos[1], penalty, is_second_symbol_next)
                case 12:
                    value_passing_fingers_call(next_pos[1], penalty, is_second_symbol_next)
        if current_pos[0] == next_pos[0]:
            match next_pos[1]:
                case 5 | 6 | 11:
                    value_passing_fingers_call(next_pos[1], abs(next_pos[0] - 2) + 1, is_second_symbol_next)
                case 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10:
                    value_passing_fingers_call(next_pos[1], abs(next_pos[0] - 2), is_second_symbol_next)
                case 12:
                    value_passing_fingers_call(next_pos[1], abs(next_pos[0] - 2) + 2, is_second_symbol_next)

    return penalty + (4 if is_second_symbol_next else 0), get_finger_by_column(next_pos[1])


def get_finger_by_column(column):
    """
    Определяет палец по колонке

    ВХОД:
        column (int): номер колонки (0-12)

    ВЫХОД:
        str: идентификатор пальца
    """
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
    """
    Подсчет пробелов

    ВХОД:
        text (str): текст для анализа

    ВЫХОД:
        None: обновляет глобальные переменные counter_fingers, counter_fingers_qwer и counter_fingers_call
    """
    spaces = text.count(' ')
    counter_fingers_qwer['f1l'] += int(spaces * 0.6)
    counter_fingers_qwer['f1r'] += int(spaces * 0.4)
    counter_fingers['f1l'] += int(spaces * 0.55)
    counter_fingers['f1r'] += int(spaces * 0.45)
    counter_fingers_call['f1l'] += int(spaces * 0.5)
    counter_fingers_call['f1r'] += int(spaces * 0.5)


def analyze_movement_details(text):
    """
    Детальный анализ перемещений для отладки

    ВХОД:
        text (str): текст для анализа

    ВЫХОД:
        list: список словарей с информацией о перемещениях
    """
    movements_info = []
    text_chars = [char for char in text.lower() if char.isalpha() or char in ' ,.']

    for i in range(1, min(50, len(text_chars))):  # Анализируем первые 50 перемещений
        current_char = text_chars[i - 1]
        next_char = text_chars[i]

        # Для раскладки Диктор
        current_pos_d = get_cords(current_char)
        next_pos_d = get_cords(next_char)
        penalty_d, finger_d = count_steps(current_char, next_char)

        # Для раскладки ЙЦУКЕН (используем копию счетчиков чтобы не дублировать)
        current_pos_q = get_cords_qwer(current_char)
        next_pos_q = get_cords_qwer(next_char)
        penalty_q, finger_q = count_steps_qwer(current_char, next_char)

        # Для раскладки Вызов
        current_pos_info_c = get_cords_vyzov(current_char)
        next_pos_info_c = get_cords_vyzov(next_char)
        penalty_c, finger_c = count_steps_call(current_char, next_char)

        # Определяем тип перемещения и информацию о втором символе
        move_type_d = get_movement_type(current_pos_d, next_pos_d) if current_pos_d and next_pos_d else "N/A"
        move_type_q = get_movement_type(current_pos_q, next_pos_q) if current_pos_q and next_pos_q else "N/A"
        move_type_c = get_movement_type(current_pos_info_c[:2] if current_pos_info_c else None,
                                        next_pos_info_c[
                                        :2] if next_pos_info_c else None) if current_pos_info_c and next_pos_info_c else "N/A"

        # Информация о втором символе для раскладки Вызов
        is_second_current = current_pos_info_c[2] if current_pos_info_c and len(current_pos_info_c) > 2 else False
        is_second_next = next_pos_info_c[2] if next_pos_info_c and len(next_pos_info_c) > 2 else False

        movements_info.append({
            'from': current_char,
            'to': next_char,
            'penalty_diktor': penalty_d,
            'penalty_qwer': penalty_q,
            'penalty_call': penalty_c,
            'finger_diktor': finger_d,
            'finger_qwer': finger_q,
            'finger_call': finger_c,
            'move_type_diktor': move_type_d,
            'move_type_qwer': move_type_q,
            'move_type_call': move_type_c,
            'pos_diktor': f"({current_pos_d[0]},{current_pos_d[1]})→({next_pos_d[0]},{next_pos_d[1]})" if current_pos_d and next_pos_d else "N/A",
            'pos_qwer': f"({current_pos_q[0]},{current_pos_q[1]})→({next_pos_q[0]},{next_pos_q[1]})" if current_pos_q and next_pos_q else "N/A",
            'pos_call': f"({current_pos_info_c[0]},{current_pos_info_c[1]})→({next_pos_info_c[0]},{next_pos_info_c[1]})" if current_pos_info_c and next_pos_info_c else "N/A",
            'second_symbol_call_current': "Да" if is_second_current else "Нет",
            'second_symbol_call_next': "Да" if is_second_next else "Нет"
        })

    return movements_info


def get_movement_type(current_pos, next_pos):
    """
    Определяет тип перемещения

    ВХОД:
        current_pos (list): текущие координаты [ряд, колонка]
        next_pos (list): следующие координаты [ряд, колонка]

    ВЫХОД:
        str: описание типа перемещения
    """
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
    """
    Печать детального анализа перемещений

    ВХОД:
        movements_info (list): список словарей с информацией о перемещениях

    ВЫХОД:
        None: выводит таблицу в консоль
    """
    print("\n" + "=" * 180)
    print("ДЕТАЛЬНЫЙ АНАЛИЗ ПЕРЕМЕЩЕНИЙ (первые 20 перемещений)")
    print("=" * 180)
    print(f"{'Переход':^10} | {'Координаты (Д)':^20} | {'Тип (Д)':^12} | {'Штраф (Д)':^9} | {'Палец (Д)':^9} | "
          f"{'Координаты (Й)':^20} | {'Тип (Й)':^12} | {'Штраф (Й)':^9} | {'Палец (Й)':^9} | "
          f"{'Координаты (В)':^20} | {'Тип (В)':^12} | {'Штраф (В)':^9} | {'Палец (В)':^9} | {'2-й символ (В)':^12}")
    print("-" * 180)

    for move in movements_info[:20]:
        second_symbol_info = f"{move['second_symbol_call_current']}→{move['second_symbol_call_next']}"
        print(f"{move['from']}→{move['to']:^7} | {move['pos_diktor']:^20} | {move['move_type_diktor']:^12} | "
              f"{move['penalty_diktor']:^9} | {move['finger_diktor']:^9} | "
              f"{move['pos_qwer']:^20} | {move['move_type_qwer']:^12} | "
              f"{move['penalty_qwer']:^9} | {move['finger_qwer']:^9} | "
              f"{move['pos_call']:^20} | {move['move_type_call']:^12} | "
              f"{move['penalty_call']:^9} | {move['finger_call']:^9} | {second_symbol_info:^12}")


def print_movement_statistics(movements_info):
    """
    Статистика по типам перемещений

    ВХОД:
        movements_info (list): список словарей с информацией о перемещениях

    ВЫХОД:
        None: выводит статистику в консоль
    """
    print("\n" + "=" * 100)
    print("СТАТИСТИКА ТИПОВ ПЕРЕМЕЩЕНИЙ")
    print("=" * 100)

    stats_diktor = {}
    stats_qwer = {}
    stats_call = {}

    for move in movements_info:
        type_d = move['move_type_diktor']
        type_q = move['move_type_qwer']
        type_c = move['move_type_call']

        stats_diktor[type_d] = stats_diktor.get(type_d, 0) + 1
        stats_qwer[type_q] = stats_qwer.get(type_q, 0) + 1
        stats_call[type_c] = stats_call.get(type_c, 0) + 1

    print(f"{'Тип перемещения':<20} | {'Диктор':<8} | {'ЙЦУКЕН':<8} | {'Вызов':<8}")
    print("-" * 60)
    all_types = set(list(stats_diktor.keys()) + list(stats_qwer.keys()) + list(stats_call.keys()))
    for move_type in sorted(all_types):
        count_d = stats_diktor.get(move_type, 0)
        count_q = stats_qwer.get(move_type, 0)
        count_c = stats_call.get(move_type, 0)
        print(f"{move_type:<20} | {count_d:<8} | {count_q:<8} | {count_c:<8}")


def print_final_results():
    """
    Печать финальных результатов

    ВХОД:
        None: использует глобальные переменные counter_fingers и counter_fingers_qwer

    ВЫХОД:
        None: выводит итоговые результаты в консоль
    """
    print("\n" + "=" * 100)
    print("ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ НАГРУЗКИ НА ПАЛЬЦЫ")
    print("=" * 100)

    print(f'\n{"":<15} | {"ДИКТОР":<15} | {"ЙЦУКЕН":<15} | {"ВЫЗОВ":<15} | {"Лучшая":<10}')
    print("-" * 80)

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
        call_val = counter_fingers_call[finger]

        # Определяем лучшую раскладку для этого пальца
        best_val = min(diktor_val, qwer_val, call_val)
        if best_val == diktor_val:
            best = "Диктор"
        elif best_val == qwer_val:
            best = "ЙЦУКЕН"
        else:
            best = "Вызов"

        print(f"{finger_names[finger]:<15} | {diktor_val:<15} | {qwer_val:<15} | {call_val:<15} | {best:<10}")

    total_diktor = sum(counter_fingers.values())
    total_qwer = sum(counter_fingers_qwer.values())
    total_call = sum(counter_fingers_call.values())

    # Определяем общую лучшую раскладку
    best_total = min(total_diktor, total_qwer, total_call)
    if best_total == total_diktor:
        best_total_name = "Диктор"
    elif best_total == total_qwer:
        best_total_name = "ЙЦУКЕН"
    else:
        best_total_name = "Вызов"

    print("-" * 80)
    print(f"{'ОБЩАЯ НАГРУЗКА':<15} | {total_diktor:<15} | {total_qwer:<15} | {total_call:<15} | {best_total_name:<10}")
    print(f"{'Эффективность':<15} | {'Лучшая' if total_diktor == best_total else 'Хуже':<15} | "
          f"{'Лучшая' if total_qwer == best_total else 'Хуже':<15} | "
          f"{'Лучшая' if total_call == best_total else 'Хуже':<15} | "
          f"{best_total_name:<10}")


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
    value_passing_fingers_call(0, len(list_upper_case) * 2)

    text_clean = ''.join(text_list)
    text_lower = [i.lower() for i in text_clean]

    # Детальный анализ (до основного подсчета)
    movements_info = analyze_movement_details(text_clean)

    # Основной анализ
    for i in range(1, len(text_lower)):
        count_steps(text_lower[i - 1], text_lower[i])
        count_steps_qwer(text_lower[i - 1], text_lower[i])
        count_steps_call(text_lower[i - 1], text_lower[i])

    # Вывод результатов
    print_detailed_analysis(movements_info)
    print_movement_statistics(movements_info)
    print_final_results()
    