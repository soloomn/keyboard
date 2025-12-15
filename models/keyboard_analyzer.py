"""
Модуль анализа и сравнения эргономики клавиатурных раскладок.

Предоставляет функционал для анализа текста с точки зрения нагрузки на пальцы
при использовании различных русскоязычных клавиатурных раскладок.

Основные возможности:
- Анализ нагрузки на каждый палец для разных раскладок
- Детальный анализ перемещений между клавишами
- Сравнительная оценка эргономичности раскладок
- Визуализация результатов анализа

Поддерживаемые раскладки:
- Диктор (diktor)
- ЙЦУКЕН (qwer)
- Вызов (vyzov)
- Ант (ant)
- Скоропись (skoropis)
- РусФон (rusphone)
- Зубачев (zubachew)

Использование:
    analyzer = LayoutAnalyzer()
    analyzer.analyze_text("Пример текста для анализа")
    analyzer.print_final_results()
"""

import re
from typing import Any, TextIO, Optional
from pathlib import Path

from models import KeyboardLayout


class LayoutAnalyzer:
    """
    Анализатор для сравнения эргономики различных клавиатурных раскладок.

    Класс выполняет статистический анализ нагрузки на пальцы и оценки
    эффективности перемещений между клавишами для разных раскладок.

    Attributes:
        layouts (dict): Словарь с экземплярами раскладок для анализа
    """

    def __init__(self, output_file: Optional[str] = None):
        """
        Инициализация анализатора с набором раскладок для сравнения.

        ВХОД:
            output_file: Optional[str] - путь к файлу для вывода результатов
                                    (по умолчанию "/app/data_output/output.txt")

        ВЫХОД:
            LayoutAnalyzer: Экземпляр анализатора с инициализированными раскладками
        """
        # Создаем экземпляры для всех раскладок
        self.layouts = {
            'diktor': KeyboardLayout("Диктор", 'diktor'),
            'qwer': KeyboardLayout("ЙЦУКЕН", 'qwer'),
            'vyzov': KeyboardLayout("Вызов", 'vyzov'),
            'ant': KeyboardLayout("ант", 'ant'),
            'skoropis': KeyboardLayout("скоропись", 'skoropis'),
            'rusphone': KeyboardLayout("русфон", 'rusphone'),
            'zubachew': KeyboardLayout("зубачев", 'zubachew')
        }

        self.twogram = {
            'udp_2gram': 0, 'chudp_2gram': 0, 'nudp_2gram': 0
        }

        self.threegram = {
            'udp_3gram': 0, 'chudp_3gram': 0, 'nudp_3gram': 0
        }

        self.fourgram = {
            'udp_4gram': 0, 'chudp_4gram': 0, 'nudp_4gram': 0
        }

        self.output_file = Path("/app/data_output/output.txt")
        # Очищаем файл при инициализации
        if self.output_file:
            self.output_file.write_text("", encoding='utf-8')

    def _print(self, text: str = "", end: str = "\n") -> None:
        """
        Внутренняя функция для вывода в console и файл одновременно.

        ВХОД:
            text: str - текст для вывода
            end: str - символ конца строки (по умолчанию "\n")

        ВЫХОД:
            None (результаты выводятся в консоль и файл)
        """
        print(text, end=end)  # В консоль

        if self.output_file:  # В файл
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(text + end)

    @property
    def reverser(self) -> dict[Any, Any]:
        """
        Свойство для получения данных о распределении пальцев по раскладкам.

        ВХОД: Нет

        ВЫХОД:
            dict: Словарь с данными о пальцах для каждой раскладки в формате:
                {
                    'layout_name': {
                        'left': [нагрузка_пальцев_левой_руки],
                        'right': [нагрузка_пальцев_правой_руки],
                        'two_handed': количество_двуручных_операций,
                        'left_press': [нажатия_пальцев_левой_руки],
                        'right_press': [нажатия_пальцев_правой_руки]
                    }
                }
        """
        all_data = {}

        for key, layout in self.layouts.items():
            all_data[key] = {
                'left': [layout.counter_fingers[f'f{i}l'] for i in range(1, 6)],
                'right': [layout.counter_fingers[f'f{i}r'] for i in range(1, 6)],
                'two_handed': layout.hand_changes,
                'left_press': [layout.key_presses[f'f{i}l'] for i in range(1, 6)],
                'right_press': [layout.key_presses[f'f{i}r'] for i in range(1, 6)]
            }

        return all_data

    @property
    def stats_reverser(self) -> dict:
        """
        Свойство для получения статистики по последовательностям (N-граммам).

        ВХОД: Нет

        ВЫХОД:
            dict: Словарь со статистикой последовательностей для каждой раскладки:
                {
                    'layout_name': {
                        "udp_2gram": одноручные удобные 2-граммы,
                        "chudp_2gram": сложные одноручные 2-граммы,
                        "nudp_2gram": разноручные 2-граммы,
                        "udp_3gram": одноручные удобные 3-граммы,
                        "chudp_3gram": сложные одноручные 3-граммы,
                        "nudp_3gram": разноручные 3-граммы,
                        "udp_4gram": одноручные удобные 4-граммы,
                        "chudp_4gram": сложные одноручные 4-граммы,
                        "nudp_4gram": разноручные 4-граммы,
                        "total_sequences": общее количество последовательностей
                    }
                }
        """
        stats = {}
        for key, layout in self.layouts.items():
            stats[key] = {
                "udp_2gram": layout.twogram["udp_2gram"],
                "chudp_2gram": layout.twogram["chudp_2gram"],
                "nudp_2gram": layout.twogram["nudp_2gram"],
                "udp_3gram": layout.threegram["udp_3gram"],
                "chudp_3gram": layout.threegram["chudp_3gram"],
                "nudp_3gram": layout.threegram["nudp_3gram"],
                "udp_4gram": layout.fourgram["udp_4gram"],
                "chudp_4gram": layout.fourgram["chudp_4gram"],
                "nudp_4gram": layout.fourgram["nudp_4gram"],
                "total_sequences": layout.total_sequences,
            }
        return stats

    def analyze_text(self, text: str) -> None:
        """
        Основной анализ текста для всех загруженных раскладок.

        ВХОД:
            text (str): Текст для анализа эргономики ввода

        ВЫХОД:
            None (результаты сохраняются во внутреннем состоянии раскладок)

        Действия функции:
            - Подсчитывает количество пробелов и заглавных букв
            - Очищает текст от нерелевантных символов
            - Анализирует перемещения между символами для каждой раскладки
            - Учитывает штрафы за использование заглавных букв
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
        """
        Детальный анализ перемещений между символами текста.

        ВХОД:
            text (str): Текст для детального анализа перемещений
            max_movements (int): Максимальное количество анализируемых перемещений
                                 (по умолчанию 50)

        ВЫХОД:
            list[dict]: Список словарей с детальной информацией о каждом перемещении:
                [
                    {
                        'from': текущий_символ,
                        'to': следующий_символ,
                        'penalty_layout': штраф_перемещения,
                        'finger_layout': используемый_палец,
                        'pos_layout': координаты_перемещения,
                        'move_type_layout': тип_перемещения,
                        ...
                    }
                ]
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
        """
        Форматирование координат для читаемого вывода.

        ВХОД:
            current_pos (list): Координаты текущей позиции [row, col, ...]
            next_pos (list): Координаты следующей позиции [row, col, ...]

        ВЫХОД:
            str: Отформатированная строка координат в формате "(row1,col1)→(row2,col2)"
                 или "N/A" если координаты не определены
        """
        if not current_pos or not next_pos:
            return "N/A"
        return f"({current_pos[0]},{current_pos[1]})→({next_pos[0]},{next_pos[1]})"

    def print_detailed_analysis(self, movements_info: list[Any], num_to_show: int = 20) -> None:
        """
        Вывод детального анализа перемещений в табличном формате.

        ВХОД:
            movements_info (list): Список данных о перемещениях от analyze_movement_details()
            num_to_show (int): Количество перемещений для отображения (по умолчанию 20)

        ВЫХОД:
            None (результаты выводятся в консоль)
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
        """
        Вывод финальных результатов анализа в табличном формате.

        ВХОД: Нет

        ВЫХОД:
            None (результаты выводятся в консоль и файл)
        """
        self._print("\n" + "=" * 100)
        self._print("ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ НАГРУЗКИ НА ПАЛЬЦЫ")
        self._print("=" * 100)

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
            self._print(row)

        # Общие результаты
        print("-" * 80)
        totals = [layout.get_total_load for layout in self.layouts.values()]
        best_total = min(totals)
        best_total_name = [layout.name for layout, total in zip(self.layouts.values(), totals) if total == best_total][0]

        total_row = f"{'ОБЩАЯ НАГРУЗКА':<15}"
        for i, layout in enumerate(self.layouts.values()):
            total_row += f" | {totals[i]:<15}"
        total_row += f" | {best_total_name:<10}"
        self._print(total_row)

        # Эффективность
        eff_row = f"{'Эффективность':<15}"
        for total in totals:
            eff_row += f" | {'Лучшая' if total == best_total else 'Хуже':<15}"
        eff_row += f" | {best_total_name:<10}"
        self._print(eff_row)

    def print_press_statistics(self) -> None:
        """
        Вывод статистики нажатий и переходов между руками.

        ВХОД: Нет

        ВЫХОД:
            None (результаты выводятся в консоль и файл)
        """
        self._print("\n" + "=" * 100)
        self._print("СТАТИСТИКА НАЖАТИЙ")
        self._print("=" * 100)

        # Статистика нажатий по пальцам
        print("\nКОЛИЧЕСТВО НАЖАТИЙ НА КАЖДЫЙ ПАЛЕЦ:")
        print("-" * 80)

        fingers = ['f1l', 'f1r', 'f2l', 'f2r', 'f3l', 'f3r', 'f4l', 'f4r', 'f5l', 'f5r']
        finger_names = {
            'f1l': 'Большой лев', 'f1r': 'Большой прав',
            'f2l': 'Указ. лев', 'f2r': 'Указ. прав',
            'f3l': 'Средний лев', 'f3r': 'Средний прав',
            'f4l': 'Безым. лев', 'f4r': 'Безым. прав',
            'f5l': 'Мизинец лев', 'f5r': 'Мизинец прав'
        }

        # Заголовок таблицы нажатий
        header = f'{"Палец":<15}'
        for layout in self.layouts.values():
            header += f" | {layout.name.upper():<15}"
        header += " | {Лучшая:<10}"
        print(header)
        print("-" * 80)

        for finger in fingers:
            row = f"{finger_names[finger]:<15}"
            values = []
            for layout in self.layouts.values():
                value = layout.get_finger_presses(finger)
                values.append(value)
                row += f" | {value:<15}"

            best_val = min(values)
            best_layouts = [layout.name for layout, val in zip(self.layouts.values(), values) if val == best_val]
            best = best_layouts[0] if best_layouts else "Нет"
            row += f" | {best:<10}"
            self._print(row)

        # Общее количество нажатий
        print("-" * 80)
        total_presses = [layout.get_total_presses for layout in self.layouts.values()]  # Убрал скобки здесь
        best_presses = min(total_presses)
        best_presses_name = [layout.name for layout, total in zip(self.layouts.values(), total_presses) if total == best_presses][0]

        total_row = f"{'ВСЕГО НАЖАТИЙ':<15}"
        for i, layout in enumerate(self.layouts.values()):
            total_row += f" | {total_presses[i]:<15}"
        total_row += f" | {best_presses_name:<10}"
        self._print(total_row)

        # Статистика переходов между руками
        self._print("\n" + "=" * 100)
        self._print("СТАТИСТИКА ПЕРЕХОДОВ")
        self._print("=" * 100)


        header = f'{"Раскладка":<15} | {"Переходы":<15} | {"% от нажатий":<15}'
        print('\n'+header)
        print("-" * 80)

        for layout_name, layout in self.layouts.items():
            hand_changes = layout.get_hand_changes
            total_presses = layout.get_total_presses  # Убрал скобки здесь
            percentage = (hand_changes / total_presses * 100) if total_presses > 0 else 0

            self._print(f"{layout.name:<15} | {hand_changes:<15} | {percentage:<15.1f}%")

        # Определение лучшей раскладки по переходам
        best_transitions = min(self.layouts.values(), key=lambda x: x.get_hand_changes)
        print(f"\nЛучшая раскладка по минимуму переходов: {best_transitions.name} "
              f"({best_transitions.get_hand_changes} переходов)")

    def analyze_sequences(self, text: str, max_sequence_length: int = 4) -> None:
        """
        Анализирует все последовательности в тексте на удобство перебора.

        ВХОД:
            text (str): Текст для анализа
            max_sequence_length (int): Максимальная длина анализируемых последовательностей
                                       (по умолчанию 4)

        ВЫХОД:
            None (результаты сохраняются во внутреннем состоянии раскладок)
        """
        # Очистка текста
        text_clean = re.sub(r'[^А-Яа-яёЁ\s]', '', text)
        text_lower = text_clean.lower()

        for layout in self.layouts.values():
            for seq_len in range(2, max_sequence_length + 1):
                for i in range(len(text_lower) - seq_len + 1):
                    sequence = text_lower[i:i + seq_len]
                    if ' ' in sequence:
                        continue
                    layout.add_sequence_result(sequence)

    def print_sequence_analysis(self) -> None:
        """
        Вывод анализа пальцевых переборов (последовательностей) в табличном формате.

        ВХОД: Нет

        ВЫХОД:
            None (результаты выводятся в консоль и файл)
        """
        self._print("\n" + "=" * 100)
        self._print("АНАЛИЗ ПАЛЬЦЕВЫХ ПЕРЕБОРОВ В РАСКЛАДКАХ")
        self._print("=" * 100)

        # Заголовки таблицы
        headers = ["Раскладка", "2г УдП", "2г ЧудП", "3г УдП", "3г ЧудП", "4г УдП", "4г ЧудП",
                   "∑ УдП", "∑ ЧудП", "∑ НудП", "Всего"]

        # Вывод заголовка таблицы
        header_line = f"{headers[0]:<12} | {headers[1]:<8} | {headers[2]:<8} | {headers[3]:<8} | " \
                      f"{headers[4]:<8} | {headers[5]:<8} | {headers[6]:<8} | " \
                      f"{headers[7]:<8} | {headers[8]:<8} | {headers[9]:<8} | {headers[10]:<8}"
        self._print(header_line)
        self._print("-" * 120)

        # Вывод данных для каждой раскладки
        for layout in self.layouts.values():
            # Получаем данные из раскладки
            udp_2gram = layout.twogram["udp_2gram"]
            chudp_2gram = layout.twogram["chudp_2gram"]
            n_2gram = layout.twogram["nudp_2gram"]

            udp_3gram = layout.threegram["udp_3gram"]
            chudp_3gram = layout.threegram["chudp_3gram"]
            n_3gram = layout.threegram["nudp_3gram"]

            udp_4gram = layout.fourgram["udp_4gram"]
            chudp_4gram = layout.fourgram["chudp_4gram"]
            n_4gram = layout.fourgram["nudp_4gram"]

            # Суммы по категориям
            total_udp = udp_2gram + udp_3gram + udp_4gram
            total_chudp = chudp_2gram + chudp_3gram + chudp_4gram
            total_nudp = n_2gram + n_3gram + n_4gram

            # Общее количество последовательностей
            total_sequences = layout.total_sequences

            # Формируем строку для вывода
            row = f"{layout.name:<12} | " \
                  f"{udp_2gram:<8} | {chudp_2gram:<8} | " \
                  f"{udp_3gram:<8} | {chudp_3gram:<8} | " \
                  f"{udp_4gram:<8} | {chudp_4gram:<8} | " \
                  f"{total_udp:<8} | {total_chudp:<8} | " \
                  f"{total_nudp:<8} | {total_sequences:<8}"

            self._print(row)

        # Дополнительная статистика: суммы по n-граммам отдельно
        self._print("\n" + "=" * 100)
        self._print("СУММАРНЫЕ ПОКАЗАТЕЛИ ПО N-ГРАММАМ")
        self._print("=" * 100)

        # Заголовки для суммарной таблицы
        sum_headers = ["Раскладка", "∑ 2-грамм", "∑ 3-грамм", "∑ 4-грамм", "∑ Однор.УдП", "∑ Однор.ЧудП", "∑ Разнор."]
        sum_header_line = f"{sum_headers[0]:<12} | {sum_headers[1]:<10} | {sum_headers[2]:<10} | " \
                          f"{sum_headers[3]:<10} | {sum_headers[4]:<12} | {sum_headers[5]:<12} | {sum_headers[6]:<10}"
        self._print(sum_header_line)
        self._print("-" * 100)

        # Вывод суммарных данных
        for layout in self.layouts.values():
            # Суммы по n-граммам
            sum_2gram = layout.twogram["udp_2gram"] + layout.twogram["chudp_2gram"]
            sum_3gram = layout.threegram["udp_3gram"] + layout.threegram["chudp_3gram"]
            sum_4gram = layout.fourgram["udp_4gram"] + layout.fourgram["chudp_4gram"]

            # Суммы по типам последовательностей
            sum_onehand_udp = (layout.twogram["udp_2gram"] + layout.threegram["udp_3gram"] +
                               layout.fourgram["udp_4gram"])
            sum_onehand_chudp = (layout.twogram["chudp_2gram"] + layout.threegram["chudp_3gram"] +
                                 layout.fourgram["chudp_4gram"])
            sum_twohand = (layout.twogram["nudp_2gram"] + layout.threegram["nudp_3gram"] +
                           layout.fourgram["nudp_4gram"])

            sum_row = f"{layout.name:<12} | " \
                      f"{sum_2gram:<10} | {sum_3gram:<10} | {sum_4gram:<10} | " \
                      f"{sum_onehand_udp:<12} | {sum_onehand_chudp:<12} | {sum_twohand:<10}"

            self._print(sum_row)

    def print_comparative_analysis(self) -> None:
        """
        Вывод сравнительного анализа всех раскладок.

        ВХОД: Нет

        ВЫХОД:
            None (результаты выводятся в консоль и файл)

        Действия функции:
            - Сравнивает раскладки по общей нагрузке, количеству нажатий и переходам
            - Выводит рейтинг раскладок по эффективности
            - Определяет лучшие раскладки по различным категориям
        """
        self._print("\n" + "=" * 100)
        self._print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ РАСКЛАДОК")
        self._print("=" * 100)

        metrics = []
        for layout_name, layout in self.layouts.items():
            metrics.append({
                'name': layout.name,
                'total_load': layout.get_total_load,
                'total_presses': layout.get_total_presses,
                'hand_changes': layout.get_hand_changes,
                'load_per_press': layout.get_total_load / layout.get_total_presses if layout.get_total_presses > 0 else 0
            })

        # Сортировка по общей нагрузке
        metrics.sort(key=lambda x: x['total_load'])

        print(f"\n{'Рейтинг':<10} | {'Раскладка':<15} | {'Общая нагрузка':<15} | {'Нажатия':<10} | "
              f"{'Переходы':<10} | {'Нагрузка/нажатие':<15}")
        print("-" * 90)

        for i, metric in enumerate(metrics, 1):
            self._print(f"{i:<10} | {metric['name']:<15} | {metric['total_load']:<15} | "
                  f"{metric['total_presses']:<10} | {metric['hand_changes']:<10} | "
                  f"{metric['load_per_press']:<15.2f}")

        # Также покажем лучшую раскладку по каждому показателю
        self._print("\n")
        self._print("=" * 100)
        self._print("ЛУЧШИЕ РАСКЛАДКИ ПО КАТЕГОРИЯМ")
        self._print("=" * 100)
        self._print("\n")

        best_by_load = min(metrics, key=lambda x: x['total_load'])
        best_by_presses = min(metrics, key=lambda x: x['total_presses'])
        best_by_changes = min(metrics, key=lambda x: x['hand_changes'])
        best_by_efficiency = min(metrics, key=lambda x: x['load_per_press'])

        self._print(f"По минимальной нагрузке: {best_by_load['name']} ({best_by_load['total_load']})")
        self._print(f"По минимальным нажатиям: {best_by_presses['name']} ({best_by_presses['total_presses']})")
        self._print(f"По минимальным переходам: {best_by_changes['name']} ({best_by_changes['hand_changes']})")
        self._print(f"По эффективности: {best_by_efficiency['name']} ({best_by_efficiency['load_per_press']:.2f})")
        self._print('\n')
