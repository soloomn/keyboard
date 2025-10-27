"""
СЛОВАРЬ КОНФИГУРАЦИИ КЛАВИАТУРНЫХ РАСКЛАДОК
-------------------------------------------

СТРУКТУРА ДАННЫХ:
-----------------
data_dict - словарь, где:
  КЛЮЧ: уникальный идентификатор клавиши (строка)
  ЗНАЧЕНИЕ: словарь с параметрами клавиши

ПАРАМЕТРЫ КЛАВИШИ:
------------------
key (str): символ(ы) в раскладке "Диктор"

qwer (str): символ(ы) в раскладке "ЙЦУКЕН"

vyzov (str): символ(ы) в раскладке "ВЫЗОВ"

raw (int): номер ряда клавиатуры (0-3), где:
  0 - верхний ряд цифр
  1 - верхний буквенный ряд
  2 - средний буквенный ряд (домашний ряд)
  3 - нижний буквенный ряд

column (int): номер колонки клавиатуры (0-12), где:
  0-1  - мизинец левой руки (f5l)
  2    - безымянный левой руки (f4l)
  3    - средний левой руки (f3l)
  4-5  - указательный левой руки (f2l)
  6-7  - указательный правой руки (f2r)
  8    - средний правой руки (f3r)
  9    - безымянный правой руки (f4r)
  10-12 - мизинец правой руки (f5r)

ОСОБЕННОСТИ:
------------
- Пустые строки "" означают отсутствие символа в данной раскладке
- Колонка 0 часто используется для служебных клавиш (пробел, регистр и т.д.)
- Ряд 2 считается "домашним" рядом (базовая позиция пальцев)
- Некоторые клавиши могут иметь multiple символов (не реализовано в текущей структуре)
"""

data_dict: dict[str, dict[str, str | int]] = {
    # === СУЩЕСТВУЮЩИЕ РАСКЛАДКИ ===
    "2": {"key": "1", "qwer": "1", "vyzov": "ё ", "ant": "!", "skoropis": ".", "rusphone": "1!", "zubachew": "1!",
          "raw": 0, "column": 1},
    "3": {"key": "2", "qwer": "2", "vyzov": "7 ", "ant": "?", "skoropis": "ё", "rusphone": "2", "zubachew": '2"',
          "raw": 0, "column": 2},
    "4": {"key": "3", "qwer": "3", "vyzov": "5 ", "ant": "'", "skoropis": "ъ", "rusphone": "3ё", "zubachew": "3",
          "raw": 0, "column": 3},
    "5": {"key": "4", "qwer": "4", "vyzov": "3 ", "ant": '"', "skoropis": "?", "rusphone": "4ё", "zubachew": "4;",
          "raw": 0, "column": 4},
    "6": {"key": "5", "qwer": "5", "vyzov": "1 ", "ant": "=", "skoropis": "!", "rusphone": "5ъ", "zubachew": "5",
          "raw": 0, "column": 5},
    "7": {"key": "6", "qwer": "6", "vyzov": "9 ", "ant": "+", "skoropis": "", "rusphone": "6ъ", "zubachew": "6:",
          "raw": 0, "column": 6},
    "8": {"key": "7", "qwer": "7", "vyzov": "0 ", "ant": "-", "skoropis": "-", "rusphone": "7", "zubachew": "7?",
          "raw": 0, "column": 7},
    "9": {"key": "8", "qwer": "8", "vyzov": "2 ", "ant": "*", "skoropis": "'", "rusphone": "8*", "zubachew": "8*",
          "raw": 0, "column": 8},
    "10": {"key": "9", "qwer": "9", "vyzov": "4 ", "ant": "/", "skoropis": "(", "rusphone": "9(", "zubachew": "9(",
           "raw": 0, "column": 9},
    "11": {"key": "0", "qwer": "0", "vyzov": "6 ", "ant": "%", "skoropis": ")", "rusphone": "0)", "zubachew": "0)",
           "raw": 0, "column": 10},
    "12": {"key": "*", "qwer": "-", "vyzov": "8 ", "ant": "(", "skoropis": "-", "rusphone": "-", "zubachew": "-",
           "raw": 0, "column": 11},
    "13": {"key": "=", "qwer": "=", "vyzov": "щ ", "ant": ")", "skoropis": "", "rusphone": "ч", "zubachew": "=+",
           "raw": 0, "column": 12},

    # === РЯД 1 (ВЕРХНИЙ РЯД) ===
    "16": {"key": "ц", "qwer": "й", "vyzov": "б ", "ant": "г", "skoropis": "ц", "rusphone": "я", "zubachew": "ф",
           "raw": 1, "column": 1},
    "17": {"key": "ь", "qwer": "ц", "vyzov": "ы ", "ant": "п", "skoropis": "ь", "rusphone": "в", "zubachew": "ы",
           "raw": 1, "column": 2},
    "18": {"key": "я", "qwer": "у", "vyzov": "о ", "ant": "р", "skoropis": "я", "rusphone": "е", "zubachew": "а",
           "raw": 1, "column": 3},
    "19": {"key": ",", "qwer": "к", "vyzov": "ую", "ant": "д", "skoropis": ",", "rusphone": "р", "zubachew": "я",
           "raw": 1, "column": 4},
    "20": {"key": ".", "qwer": "е", "vyzov": "ь ", "ant": "м", "skoropis": ".", "rusphone": "т", "zubachew": ",ъ",
           "raw": 1, "column": 5},
    "21": {"key": "з", "qwer": "н", "vyzov": "ё ", "ant": "ы", "skoropis": "з", "rusphone": "ы", "zubachew": "й",
           "raw": 1, "column": 6},
    "22": {"key": "в", "qwer": "г", "vyzov": "л ", "ant": "и", "skoropis": "в", "rusphone": "у", "zubachew": "м",
           "raw": 1, "column": 7},
    "23": {"key": "к", "qwer": "ш", "vyzov": "д ", "ant": "я", "skoropis": "к", "rusphone": "и", "zubachew": "р",
           "raw": 1, "column": 8},
    "24": {"key": "д", "qwer": "щ", "vyzov": "я ", "ant": "у", "skoropis": "д", "rusphone": "о", "zubachew": "п",
           "raw": 1, "column": 9},
    "25": {"key": "ч", "qwer": "з", "vyzov": "г ", "ant": "х", "skoropis": "ч", "rusphone": "п", "zubachew": "х",
           "raw": 1, "column": 10},
    "26": {"key": "ш", "qwer": "х", "vyzov": "ж ", "ant": "ц", "skoropis": "ш", "rusphone": "ш", "zubachew": "ц",
           "raw": 1, "column": 11},
    "27": {"key": "щ", "qwer": "ъ", "vyzov": "ц ", "ant": "ж", "skoropis": "щ", "rusphone": "щ", "zubachew": "щ",
           "raw": 1, "column": 12},

    # === РЯД 2 (СРЕДНИЙ РЯД, ДОМАШНИЙ) ===
    "30": {"key": "у", "qwer": "ф", "vyzov": "чц", "ant": "в", "skoropis": "у", "rusphone": "а", "zubachew": "г",
           "raw": 2, "column": 1},
    "31": {"key": "и", "qwer": "ы", "vyzov": "и ", "ant": "н", "skoropis": "и", "rusphone": "с", "zubachew": "и",
           "raw": 2, "column": 2},
    "32": {"key": "е", "qwer": "в", "vyzov": "еэ", "ant": "с", "skoropis": "е", "rusphone": "д", "zubachew": "е",
           "raw": 2, "column": 3},
    "33": {"key": "о", "qwer": "а", "vyzov": "а ", "ant": "т", "skoropis": "о", "rusphone": "ф", "zubachew": "о",
           "raw": 2, "column": 4},
    "34": {"key": "а", "qwer": "п", "vyzov": "  ", "ant": "л", "skoropis": "а", "rusphone": "г", "zubachew": "у",
           "raw": 2, "column": 5},
    "35": {"key": "л", "qwer": "р", "vyzov": "  ", "ant": "ь", "skoropis": "л", "rusphone": "х", "zubachew": "л",
           "raw": 2, "column": 6},
    "36": {"key": "н", "qwer": "о", "vyzov": "нщ", "ant": "о", "skoropis": "н", "rusphone": "й", "zubachew": "т",
           "raw": 2, "column": 7},
    "37": {"key": "т", "qwer": "л", "vyzov": "тъ", "ant": "е", "skoropis": "т", "rusphone": "к", "zubachew": "с",
           "raw": 2, "column": 8},
    "38": {"key": "с", "qwer": "д", "vyzov": "с ", "ant": "а", "skoropis": "с", "rusphone": "л", "zubachew": "н",
           "raw": 2, "column": 9},
    "39": {"key": "р", "qwer": "ж", "vyzov": "в ", "ant": "к", "skoropis": "р", "rusphone": ";:", "zubachew": "з",
           "raw": 2, "column": 10},
    "40": {"key": "й", "qwer": "э", "vyzov": "з ", "ant": "з", "skoropis": "й", "rusphone": "'", "zubachew": "ж",
           "raw": 2, "column": 11},
    "41": {"key": "ё", "qwer": "ё", "vyzov": "ю ", "ant": "", "skoropis": "*", "rusphone": "ю",
           "zubachew": "ё", "raw": 0, "column": 0},

    # === РЯД 3 (НИЖНИЙ РЯД) ===
    "44": {"key": "ф", "qwer": "я", "vyzov": "ш ", "ant": "щ", "skoropis": "ф", "rusphone": "з", "zubachew": "ш",
           "raw": 3, "column": 1},
    "45": {"key": "э", "qwer": "ч", "vyzov": "х ", "ant": "й", "skoropis": "э", "rusphone": "ь", "zubachew": "ьъ",
           "raw": 3, "column": 2},
    "46": {"key": "х", "qwer": "с", "vyzov": "й ", "ant": "ш", "skoropis": "х", "rusphone": "ц", "zubachew": "ю",
           "raw": 3, "column": 3},
    "47": {"key": "ы", "qwer": "м", "vyzov": "к ", "ant": "б", "skoropis": "ы", "rusphone": "ж", "zubachew": ".ь",
           "raw": 3, "column": 4},
    "48": {"key": "ю", "qwer": "и", "vyzov": "  ", "ant": ",;", "skoropis": "ю", "rusphone": "б", "zubachew": "э",
           "raw": 3, "column": 5},
    "49": {"key": "б", "qwer": "т", "vyzov": "э ", "ant": ".:", "skoropis": "б", "rusphone": "н", "zubachew": "б",
           "raw": 3, "column": 6},
    "50": {"key": "м", "qwer": "ь", "vyzov": "рц", "ant": "ю", "skoropis": "м", "rusphone": "м", "zubachew": "д",
           "raw": 3, "column": 7},
    "51": {"key": "п", "qwer": "б", "vyzov": "м ", "ant": "э", "skoropis": "п", "rusphone": ".<", "zubachew": "в",
           "raw": 3, "column": 8},
    "52": {"key": "г", "qwer": "ю", "vyzov": "ф ", "ant": "ё", "skoropis": "г", "rusphone": ",>", "zubachew": "к",
           "raw": 3, "column": 9},
    "53": {"key": "ж", "qwer": ".", "vyzov": "п ", "ant": "ф", "skoropis": "ж", "rusphone": "/?", "zubachew": "ч",
           "raw": 3, "column": 10},
    "54": {"key": "", "qwer": "", "vyzov": "  ", "ant": "", "skoropis": "", "rusphone": "",
           "zubachew": "", "raw": 3, "column": 11},

    # === ПРОБЕЛ И СЛУЖЕБНЫЕ КЛАВИШИ ===
    "14": {"key": "ъ", "qwer": "", "vyzov": "  ", "ant": "", "skoropis": "", "rusphone": "", "zubachew": "", "raw": 0,
           "column": 0},
    "15": {"key": " ", "qwer": "", "vyzov": "  ", "ant": "", "skoropis": "", "rusphone": "", "zubachew": "", "raw": 0,
           "column": 0},
    "28": {"key": "", "qwer": "", "vyzov": "  ", "ant": "", "skoropis": "", "rusphone": "", "zubachew": "", "raw": 0,
           "column": 0},
    "29": {"key": "", "qwer": ",", "vyzov": "  ", "ant": "", "skoropis": "", "rusphone": "", "zubachew": "", "raw": 0,
           "column": 0},
    "42": {"key": "", "qwer": "", "vyzov": "  ", "ant": "", "skoropis": "", "rusphone": "", "zubachew": "", "raw": 0,
           "column": 0},
    "43": {"key": "", "qwer": "", "vyzov": "ъ ", "ant": "", "skoropis": "", "rusphone": "", "zubachew": "", "raw": 0,
           "column": 0},
    "55": {"key": "", "qwer": "", "vyzov": "  ", "ant": "ч", "skoropis": '"', "rusphone": "э", "zubachew": "", "raw": 1,
           "column": 13},
    "56": {"key": "", "qwer": "", "vyzov": "  ", "ant": "", "skoropis": "", "rusphone": "", "zubachew": "", "raw": 0,
           "column": 0},
    "57": {"key": " ", "qwer": " ", "vyzov": "  ", "ant": " ", "skoropis": " ", "rusphone": " ", "zubachew": " ",
           "raw": 0, "column": 0},
    "58": {"key": "", "qwer": "", "vyzov": "  ", "ant": "", "skoropis": "", "rusphone": "", "zubachew": "", "raw": 0,
           "column": 0}
}
