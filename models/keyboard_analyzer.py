import re
from typing import Any

from models import KeyboardLayout


class LayoutAnalyzer:
    """Класс для анализа и сравнения раскладок"""

    def __init__(self):
        """

        """
        # Создаем экземпляры для всех раскладок
        self.layouts = {
            'diktor': KeyboardLayout("Диктор", 'diktor'),
            'qwer': KeyboardLayout("ЙЦУКЕН", 'qwer'),
            'vyzov': KeyboardLayout("Вызов", 'vyzov')
        }

    @property
    def reverser(self) -> dict[Any, Any]:
        """

        :rtype: dict[Any, Any]
        :return:
        """
        all_data = {}

        for key, layout in self.layouts.items():
            all_data[key] = {
                'left': [layout.counter_fingers[f'f{i}l'] for i in range(1, 6)],
                'right': [layout.counter_fingers[f'f{i}r'] for i in range(1, 6)]
            }

        return all_data

    def analyze_text(self, text: str) -> None:
        """Анализ текста для всех раскладок
        :rtype: None
        :param text:
        """
        # Обработка пробелов
        spaces_count = text.count(' ')
        for layout in self.layouts.values():
            layout.count_spaces(spaces_count)

        # Очистка текста
        text_clean = re.sub(r'[^А-Яа-яёЁ1-9,0\s]', '', text)
        text_lower = [i.lower() for i in text_clean]

        # Учет заглавных букв
        uppercase_count = len([i for i in text if i.isupper()])
        for layout in self.layouts.values():
            layout.add_uppercase_penalty(uppercase_count)

        # Основной анализ перемещений
        for i in range(1, len(text_lower)):
            for layout in self.layouts.values():
                layout.count_steps(text_lower[i - 1], text_lower[i])

    def analyze_movement_details(self, text: str, max_movements: int = 50) -> list[Any]:
        """Детальный анализ перемещений
        :rtype: list[Any]
        :param text: 
        :param max_movements: 
        :return: 
        """
        movements_info = []
        text_chars = [char for char in text.lower() if char.isalpha() or char in ' ,.']

        for i in range(1, min(max_movements, len(text_chars))):
            current_char = text_chars[i - 1]
            next_char = text_chars[i]

            movement_data = {'from': current_char, 'to': next_char}

            for layout_name, layout in self.layouts.items():
                current_pos = layout.get_coords(current_char)
                next_pos = layout.get_coords(next_char)
                penalty, finger = layout.count_steps(current_char, next_char)

                # Сохраняем данные для этого перехода
                movement_data[f'penalty_{layout_name}'] = str(penalty)
                movement_data[f'finger_{layout_name}'] = finger
                movement_data[f'pos_{layout_name}'] = self.format_coords(current_pos, next_pos)
                movement_data[f'move_type_{layout_name}'] = layout.get_movement_type(current_pos, next_pos)

                # Информация о втором символе (актуально для Вызов)
                if layout_name == 'vyzov' and current_pos and next_pos:
                    movement_data['second_symbol_current'] = "Да" if len(current_pos) > 2 and current_pos[2] else "Нет"
                    movement_data['second_symbol_next'] = "Да" if len(next_pos) > 2 and next_pos[2] else "Нет"

            movements_info.append(movement_data)

        return movements_info

    @staticmethod
    def format_coords(current_pos: list[str | int | bool], next_pos: list[str | int | bool]) -> str:
        """Форматирование координат для вывода
        :rtype: str
        :param current_pos: 
        :param next_pos: 
        :return: 
        """
        if not current_pos or not next_pos:
            return "N/A"
        return f"({current_pos[0]},{current_pos[1]})→({next_pos[0]},{next_pos[1]})"

    def print_detailed_analysis(self, movements_info: list[Any], num_to_show: int = 20) -> None:
        """Печать детального анализа
        :rtype: None
        :param movements_info: 
        :param num_to_show: 
        """
        print("\n" + "=" * 180)
        print(f"ДЕТАЛЬНЫЙ АНАЛИЗ ПЕРЕМЕЩЕНИЙ (первые {num_to_show} перемещений)")
        print("=" * 180)

        # Формируем заголовки
        headers = [f"{'Переход':^10}"]
        layout_headers = ['Координаты', 'Тип', 'Штраф', 'Палец']

        for layout_name in self.layouts.keys():
            layout_display = layout_name[0].upper()  # Д, Й, В
            for header in layout_headers:
                headers.append(f"{header} ({layout_display}):^20")

        headers.append(f"{'2-й символ':^12}")
        print(" | ".join(headers))
        print("-" * 180)

        # Выводим данные
        for move in movements_info[:num_to_show]:
            row = [f"{move['from']}→{move['to']:^7}"]

            for layout_name in self.layouts.keys():
                row.extend([
                    f"{move[f'pos_{layout_name}']:^20}",
                    f"{move[f'move_type_{layout_name}']:^20}",
                    f"{move[f'penalty_{layout_name}']:^20}",
                    f"{move[f'finger_{layout_name}']:^20}"
                ])

            # Информация о втором символе (для Вызов)
            second_symbol = f"{move.get('second_symbol_current', 'Нет')}→{move.get('second_symbol_next', 'Нет')}"
            row.append(f"{second_symbol:^12}")

            print(" | ".join(row))

    def print_final_results(self) -> None:
        """Печать финальных результатов
        :rtype: None
        """
        print("\n" + "=" * 100)
        print("ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ НАГРУЗКИ НА ПАЛЬЦЫ")
        print("=" * 100)

        # Заголовок таблицы
        header = f'\n{"":<15}'
        for layout in self.layouts.values():
            header += f" | {layout.name.upper():<15}"
        header += " | {Лучшая:<10}"
        print(header)
        print("-" * 80)

        fingers = ['f1l', 'f1r', 'f2l', 'f2r', 'f3l', 'f3r', 'f4l', 'f4r', 'f5l', 'f5r']
        finger_names = {
            'f1l': 'Большой лев', 'f1r': 'Большой прав',
            'f2l': 'Указ. лев', 'f2r': 'Указ. прав',
            'f3l': 'Средний лев', 'f3r': 'Средний прав',
            'f4l': 'Безым. лев', 'f4r': 'Безым. прав',
            'f5l': 'Мизинец лев', 'f5r': 'Мизинец прав'
        }

        # Данные по пальцам
        for finger in fingers:
            row = f"{finger_names[finger]:<15}"
            values = []
            for layout in self.layouts.values():
                value = layout.get_finger_load(finger)
                values.append(value)
                row += f" | {value:<15}"

            best_val = min(values)
            best_layouts = [layout.name for layout, val in zip(self.layouts.values(), values) if val == best_val]
            best = best_layouts[0] if best_layouts else "Нет"
            row += f" | {best:<10}"
            print(row)

        # Общие результаты
        print("-" * 80)
        totals = [layout.get_total_load for layout in self.layouts.values()]
        best_total = min(totals)
        best_total_name = [layout.name for layout, total in zip(self.layouts.values(), totals) if total == best_total][
            0]

        total_row = f"{'ОБЩАЯ НАГРУЗКА':<15}"
        for i, layout in enumerate(self.layouts.values()):
            total_row += f" | {totals[i]:<15}"
        total_row += f" | {best_total_name:<10}"
        print(total_row)

        # Эффективность
        eff_row = f"{'Эффективность':<15}"
        for total in totals:
            eff_row += f" | {'Лучшая' if total == best_total else 'Хуже':<15}"
        eff_row += f" | {best_total_name:<10}"
        print(eff_row)
