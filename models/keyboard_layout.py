"""
Модуль представления клавиатурной раскладки и расчета эргономических показателей.

Содержит класс KeyboardLayout для работы с различными типами раскладок клавиатуры,
расчета нагрузки на пальцы и оценки эффективности перемещений между клавишами.

Основные функции:
- Определение координат символов для разных раскладок
- Расчет штрафов за перемещения между клавишами
- Распределение нагрузки по пальцам
- Анализ типов перемещений
"""

from data import data_dict


class KeyboardLayout:
    """
    Класс для представления клавиатурной раскладки и расчета эргономических показателей.

    Обеспечивает функционал для работы с различными типами раскладок (ЙЦУКЕН, Диктор, Вызов),
    включая расчет координат символов, штрафов за перемещения и распределения нагрузки по пальцам.

    Attributes:
        name (str): Название раскладки
        layout_type (str): Тип раскладки ('diktor', 'qwer', 'vyzov')
        counter_fingers (dict): Счетчик нагрузки на каждый палец
    """

    def __init__(self, name: str, layout_type: str) -> None:
        """
        Инициализация раскладки клавиатуры.

        ВХОД:
            name (str): Человеко-читаемое название раскладки
            layout_type (str): Тип раскладки ('diktor', 'qwer', 'vyzov')

        ВЫХОД: Нет
        """
        self.name = name
        self.layout_type = layout_type  # 'diktor', 'qwer', 'vyzov'
        self.counter_fingers = {
            'f5l': 0, 'f4l': 0, 'f3l': 0, 'f2l': 0, 'f1l': 0,
            'f1r': 0, 'f2r': 0, 'f3r': 0, 'f4r': 0, 'f5r': 0
        }

    @property
    def get_symbol_field(self) -> str:
        """
        Получение названия поля с символами для данной раскладки.

        ВХОД: Нет

        ВЫХОД:
            str: Название поля в data_dict для данной раскладки
        """
        if self.layout_type == 'diktor':
            return 'key'
        elif self.layout_type == 'qwer':
            return 'qwer'
        elif self.layout_type == 'vyzov':
            return 'vyzov'
        return 'key'

    def get_coords(self, symbol: str) -> list[str | int | bool] | None:
        """
        Получение координат символа в текущей раскладке.

        ВХОД:
            symbol (str): Символ для поиска координат

        ВЫХОД:
            list | None: Список с координатами [row, column, is_second_symbol, additional_penalty]
                       или None если символ не найден
        """
        field_name = self.get_symbol_field

        for key in data_dict:
            chars = data_dict[key][field_name]

            # Для раскладки Вызов обрабатываем специально многосимвольные клавиши
            if self.layout_type == 'vyzov':
                chars = chars.strip()
                if len(chars) == 2:
                    # Клавиша с двумя символами
                    if chars[0] == symbol:
                        return [data_dict[key]['raw'], data_dict[key]['column'], False, 0]  # Первый символ
                    elif chars[1] == symbol:
                        return [data_dict[key]['raw'], data_dict[key]['column'], True, 4]  # Второй символ + штраф
                elif len(chars) == 1:
                    # Клавиша с одним символом
                    if chars[0] == symbol:
                        return [data_dict[key]['raw'], data_dict[key]['column'], False, 0]
            else:
                # Для обычных раскладок
                for value in chars:
                    if value == symbol:
                        return [data_dict[key]['raw'], data_dict[key]['column'], False, 0]
        return None

    @staticmethod
    def calculate_penalty(current_pos: list[int], next_pos: list[int]) -> int:
        """
        Расчет штрафа за перемещение между двумя позициями.

        ВХОД:
            current_pos (list): Текущая позиция [row, column]
            next_pos (list): Следующая позиция [row, column]

        ВЫХОД:
            int: Штраф за перемещение (0-4 балла)
        """
        if not current_pos or not next_pos:
            return 0

        # Извлекаем координаты (первые два элемента)
        current_row, current_col = current_pos[0], current_pos[1]
        next_row, next_col = next_pos[0], next_pos[1]

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

    @staticmethod
    def get_finger_by_column(column: int) -> str:
        """
        Определение пальца, отвечающего за колонку клавиатуры.

        ВХОД:
            column (int): Номер колонки клавиатуры (0-12)

        ВЫХОД:
            str: Идентификатор пальца ('f1l', 'f2r', и т.д.)
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

    def apply_finger_load(self, column: int, penalty_value: int, additional_penalty: int = 0) -> None:
        """
        Применение нагрузки к соответствующему пальцу.

        ВХОД:
            column (int): Колонка клавиатуры
            penalty_value (int): Основной штраф за перемещение
            additional_penalty (int): Дополнительный штраф

        ВЫХОД: Нет
        """
        total_value = penalty_value + additional_penalty

        match column:
            case 0 | 1:
                self.counter_fingers['f5l'] += total_value
            case 2:
                self.counter_fingers['f4l'] += total_value
            case 3:
                self.counter_fingers['f3l'] += total_value
            case 4 | 5:
                self.counter_fingers['f2l'] += total_value
            case 6 | 7:
                self.counter_fingers['f2r'] += total_value
            case 8:
                self.counter_fingers['f3r'] += total_value
            case 9:
                self.counter_fingers['f4r'] += total_value
            case 10 | 11 | 12:
                self.counter_fingers['f5r'] += total_value

    def count_steps(self, first_sim: str, second_sim: str) -> tuple[int, str]:
        """
        Подсчет шагов и штрафов между двумя символами.

        ВХОД:
            first_sim (str): Первый символ
            second_sim (str): Второй символ

        ВЫХОД:
            tuple: (total_penalty, finger) - общий штраф и используемый палец
        """
        current_pos_info = self.get_coords(first_sim)
        next_pos_info = self.get_coords(second_sim)

        if not current_pos_info or not next_pos_info:
            return 0, 'N/A'

        # Извлекаем информацию о позициях
        current_pos = current_pos_info[:2]  # row, column
        next_pos = next_pos_info[:2]  # row, column

        # Извлекаем информацию о втором символе и дополнительном штрафе
        is_second_symbol_current = current_pos_info[2] if len(current_pos_info) > 2 else False
        is_second_symbol_next = next_pos_info[2] if len(next_pos_info) > 2 else False
        additional_penalty_current = current_pos_info[3] if len(current_pos_info) > 3 else 0
        additional_penalty_next = next_pos_info[3] if len(next_pos_info) > 3 else 0

        # Расчет штрафа за перемещение
        penalty = self.calculate_penalty(current_pos, next_pos)

        # Общий штраф = штраф_перемещения + штраф_второго_символа_конечной_позиции
        total_penalty = penalty + additional_penalty_next

        # Применяем нагрузку к пальцам
        self.apply_movement_penalty(current_pos, next_pos, penalty, additional_penalty_next)

        return total_penalty, self.get_finger_by_column(next_pos[1])

    def apply_movement_penalty(self, current_pos: list[str | int | bool], next_pos: list[str | int | bool],
                               penalty: int,
                               additional_penalty: int) -> None:
        """
        Применение штрафа за перемещение с учетом типа движения.

        ВХОД:
            current_pos (list): Текущая позиция [row, column]
            next_pos (list): Следующая позиция [row, column]
            penalty (int): Основной штраф за перемещение
            additional_penalty (int): Дополнительный штраф

        ВЫХОД: Нет
        """
        current_row, current_col = current_pos
        next_row, next_col = next_pos

        total_penalty = penalty + additional_penalty

        if current_col == next_col:
            # Вертикальное перемещение
            self.apply_finger_load(next_col, penalty, additional_penalty)
        else:
            if current_row != next_row:
                # Диагональное или сложное перемещение
                match next_col:
                    case 5 | 6:
                        if next_row == 2:
                            self.apply_finger_load(next_col, 1, additional_penalty)
                        else:
                            self.apply_finger_load(next_col, penalty, additional_penalty)
                    case 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10:
                        if next_row == 2:
                            self.apply_finger_load(next_col, 0, additional_penalty)
                        else:
                            self.apply_finger_load(next_col, penalty, additional_penalty)
                    case 11:
                        self.apply_finger_load(next_col, penalty, additional_penalty)
                    case 12:
                        self.apply_finger_load(next_col, penalty, additional_penalty)

            if current_row == next_row:
                # Горизонтальное перемещение
                match next_col:
                    case 5 | 6 | 11:
                        self.apply_finger_load(next_col, abs(next_row - 2) + 1, additional_penalty)
                    case 1 | 2 | 3 | 4 | 7 | 8 | 9 | 10:
                        self.apply_finger_load(next_col, abs(next_row - 2), additional_penalty)
                    case 12:
                        self.apply_finger_load(next_col, abs(next_row - 2) + 2, additional_penalty)

    @staticmethod
    def get_movement_type(current_pos: list[str | int | bool], next_pos: list[str | int | bool]) -> str:
        """
        Определение типа перемещения между позициями.

        ВХОД:
            current_pos (list): Текущая позиция [row, column, ...]
            next_pos (list): Следующая позиция [row, column, ...]

        ВЫХОД:
            str: Описание типа перемещения
        """
        if not current_pos or not next_pos:
            return "N/A"

        # Берем только координаты (первые два элемента)
        current_coords = current_pos[:2]
        next_coords = next_pos[:2]

        row_diff = abs(current_coords[0] - next_coords[0])
        col_diff = abs(current_coords[1] - next_coords[1])

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

    def count_spaces(self, spaces_count: int) -> None:
        """
        Распределение нагрузки от пробелов по большим пальцам.

        ВХОД:
            spaces_count (int): Количество пробелов в тексте

        ВЫХОД: Нет
        """
        if self.layout_type == 'qwer':
            self.counter_fingers['f1l'] += int(spaces_count * 0.6)
            self.counter_fingers['f1r'] += int(spaces_count * 0.4)
        elif self.layout_type == 'diktor':
            self.counter_fingers['f1l'] += int(spaces_count * 0.55)
            self.counter_fingers['f1r'] += int(spaces_count * 0.45)
        else:  # vyzov
            self.counter_fingers['f1l'] += int(spaces_count * 0.5)
            self.counter_fingers['f1r'] += int(spaces_count * 0.5)

    def add_uppercase_penalty(self, uppercase_count: int) -> None:
        """
        Добавление штрафа за использование заглавных букв.

        ВХОД:
            uppercase_count (int): Количество заглавных букв

        ВЫХОД: Нет
        """
        penalty = uppercase_count * 2
        self.apply_finger_load(0, penalty)

    @property
    def get_total_load(self) -> int:
        """
        Получение общей нагрузки на все пальцы.

        ВХОД: Нет

        ВЫХОД:
            int: Суммарная нагрузка на все пальцы
        """
        return sum(self.counter_fingers.values())

    def get_finger_load(self, finger: str) -> int:
        """
        Получение нагрузки на конкретный палец.

        ВХОД:
            finger (str): Идентификатор пальца ('f1l', 'f2r', и т.д.)

        ВЫХОД:
            int: Нагрузка на указанный палец
        """
        return self.counter_fingers.get(finger, 0)
