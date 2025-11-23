<h1 align="center">KEYBOARD</h1>

<h6 align="center">
Transforming typing for a healthier, smarter future.
</h6>

|          |                                                                                                                                                                                                                                        |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Bio      | ![top_Lang](https://img.shields.io/github/languages/top/soloomn/keyboard?style=flat&logo=python&logoColor=white&color=0080ff) ![langs](https://img.shields.io/github/languages/count/soloomn/keyboard?style=flat&color=0080ff)         |
| Testing  | [![CI - Test](https://github.com/soloomn/keyboard/actions/workflows/tests.yml/badge.svg)](https://github.com/soloomn/keyboard/actions/workflows/tests.yml)                                                                             |
| Coverage | ![Coverage](https://img.shields.io/badge/coverage-47%25-yellow)                                                                                                                                                                        |
| Package  | ![Last-Commit](https://img.shields.io/github/last-commit/soloomn/keyboard?style=flat&logo=git&logoColor=white&color=0080ff) ![release](https://img.shields.io/github/v/tag/soloomn/keyboard.svg?label=Release&style=flat&color=0080ff) |
| License  | ![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

<h6 align="center">
Built with the tools and technologies:
</h6>


|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Languages    | ![python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=000&style=flat-square) ![HTML5](https://img.shields.io/badge/HTML-%23E34F26.svg?logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS-639?logo=css&logoColor=fff)                                                                                                                   |
| Services     | ![docker](https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white)  ![poetry](https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat&logo=Poetry&logoColor=white) ![pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat&logo=Pytest&logoColor=white) ![sphinx](https://img.shields.io/badge/Sphinx-000000.svg?style=flat&logo=Sphinx&logoColor=white)                                                                                       |
| Technologies | ![redis](https://img.shields.io/badge/Redis-FF4438.svg?style=flat&logo=Redis&logoColor=white) ![rabbitmq](https://img.shields.io/badge/RabbitMQ-FF6600.svg?style=flat&logo=RabbitMQ&logoColor=white)                                                                                                                                                                                                                                                                                       |
| Core         | ![numpy](https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white) ![seaborn](https://custom-icon-badges.demolab.com/badge/Seaborn-CBC3E3?logo=seaborn) ![matplotlib](https://custom-icon-badges.demolab.com/badge/Matplotlib-71D291?logo=matplotlib&logoColor=fff) ![rich](https://img.shields.io/badge/Rich-FAE742.svg?style=flat&logo=Rich&logoColor=black) |
| Web core     | ![fastapi](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white) ![websocket](https://custom-icon-badges.demolab.com/badge/WebSocket-177245?logo=websocket) ![pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=Pydantic&logoColor=white)                                                                                                                                                                                                                |
| CI           | ![githubactions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white)                                                                                                                                                                                                                                                                                                                                                                  |


---

## Table of Contents

- [Overview](#overview)
  - [Case definition](#case-definition)
  - [Overall project description](#overall-project-description)
  - [Principal purpose](#principal-purpose)
  - [Key features](#key-features)
  - [Contex & actuality](#context-and-actuality)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)
- [Technical Overview](#technical-overview)
  - [Solution Architecture](#solution-architecture)
  - [Metrics & Data processing](#metrics-and-data-processing)
  - [Results & its practical relevance](#results-and-its-practical-relevance)

---

## Overview

**Задача: оптимизация русских раскладок**

### Case definition
Разработать функционал для автоматизированной оптимизации существующих
клавиатурных раскладок на основе заданных эргономических 
критериев и статистики реального текста.

---

### Overall project description
Данный проект представляет собой инструмент для сравнительного анализа эргономичности различных 
русских клавиатурных раскладок. Программа оценивает эффективность семи раскладок на основе анализа реального текста.
Анализируемые раскладки:
1)  <ins>**ЙЦУКЕН**</ins> - стандартная раскладка
2)  <ins>**Диктор**</ins> - оптимизированная для частотности букв
3)  <ins>**Вызов**</ins> - радикальный подход с двухсимвольными клавишами
4)  <ins>**Зубачёв**</ins> - эргономичная раскладка Сергея Зубачёва
5)  <ins>**Скоропись**</ins> - раскладка для скоростной печати
6)  <ins>**Русская фонетическая**</ins> - основанная на фонетическом принципе
7)  <ins>**АНТ**</ins> - антропоморфная типографская раскладка

---

### Principal purpose
Определить наиболее эргономичную русскую раскладку клавиатуры путем комплексного анализа:
1)  Штрафных баллов за перемещения между клавишами
2)  Распределения нагрузки на пальцы рук
3)  Статистики типов перемещений

---

### Key features
1)  *Многофакторный анализ*: учитывает не только расстояние между клавишами, но и тип перемещений
2)  *Детальная статистика*: предоставляет подробную информацию по каждому аспекту эргономики
3)  *Визуализация результатов*: удобное табличное представление данных
4)  *Гибкая система штрафов*: адаптивная система оценки сложности перемещений

---

### Context and actuality
**Проблема стандартной раскладки ЙЦУКЕН:**
анализ дискуссий в профессиональном сообществе показывает, что ЙЦУКЕН часто критикуют за:
- <ins>**Неоптимальное распределение частотных букв**</ins>
1)  Критики отмечают, что частотные буквы русского языка расположены в неудобных позициях
2) Высокая нагрузка на мизинцы и слабые пальцы
3)  Неравномерное распределение между руками
- <ins>**Историческая наследуемость**</ins>
1)  Раскладка создавалась для механических пишущих машинок
2)  Современные электронные клавиатуры не имеют технических ограничений тех лет
3)  Сохраняется компромиссный характер из-за обратной совместимости

<h4>Альтернативные подходы:</h4>

- <ins>**Раскладка "Диктор"**</ins>
1) Разрабатывалась с учетом частотности русских букв
2)  Позиционируется как оптимизированная для слепой печати
3)  Учитывает эргономические принципы распределения нагрузки
- <ins>**Раскладка "Вызов"**</ins>
1)  Предлагает радикально новый подход к организации символов
2)  Включает двухсимвольные клавиши для редких букв
3)  Фокусируется на минимизации перемещений пальцев
- <ins>**Зубачёв:**</ins>
1)  Разработана с учетом биомеханики рук
2)  Оптимизированное распределение нагрузки по пальцам
3)  Учет частотности русских букв
- <ins>**Скоропись:**</ins>
1)  Специализирована для высокой скорости набора
2)  Минимизация сложных перемещений
3)  Акцент на "домашней" позиции пальцев
- <ins>**Русская фонетическая:**</ins>
1)  Логическое расположение букв по фонетическому принципу
2)  Упрощение запоминания для новичков
3)  Сопоставление звуков и расположения
- <ins>**АНТ (антропоморфная типографская):**</ins>
1)  Учет антропометрических особенностей рук
2)  Оптимизация под русскую типографику
3)  Баланс между комфортом и скоростью    


---

## Getting Started

### Prerequisites

Проект использует следующие зависимости:

- **Programming Language:** Python 3.12.3
- **Package Manager:** poetry
- **Container Runtime:** Docker
- **Infrastructure:**
  - Redis (for result storage)
  - RabbitMQ (for distributed processing)
- **Input corpus:** 
  - `voina-i-mir.txt` (War and Peace by Leo Tolstoy, Russian text)
  - `1grams-3.txt`
  - `sortchbukw.csv`
---

### Installation

Соберите и настройте `keyboard`:

1. **Клонируйте репозиторий:**

   ```
   git clone https://github.com/soloomn/keyboard
   cd keyboard
   ```

2. **Установите зависимости**

   Используя **poetry**:

   ```
   poetry install
   ```



3. **Постройте Docker image**

   ```
   docker-compose build base
   docker-compose build
   ```

---

### Usage

Запустите анализ.

Используя **Docker-compose**:

```
docker-compose up
```

Основные параметры конфигурации:

- Раскладка клавиатуры и координаты определяются в файле `dictr.py`.
- Путь к текстовому корпусу и среда (Redis, RabbitMQ и т. д.) настраиваются с помощью переменных среды.
- Параметры анализа (штрафы, размер блока и т. д.) устанавливаются в ядре модуля analyzer.

---

### Testing

`keyboard` использует стандартный стек Python для тестирования (pytest / pytest-cov / unittest).

Используя **Docker**:

```
docker-compose up
docker-compose run --rm analyzer pytest tests/ --maxfail=1 --disable-warnings -q
```

Используя **poetry**:

```
poetry run pytest
```

Или запустите для отдельных модулей:

```
python -m unittest test_keyboard_analyzer.py
python -m unittest test_keyboard_layout.py
python -m unittest test_utils_stats.py
python -m unittest test_integration.py
```

---

## Technical Overview

### Solution architecture

Проект имеет модульную архитектуру с четким разделением ответственности.
Основные модули анализа:
- <ins>**Модели данных и ядро анализа:**</ins>
1)  *keyboard_layout.py* - базовый класс *KeyboardLayout* для представления раскладки
2)  *keyboard_analyzer.py* - основной анализатор *LayoutAnalyzer* для сравнения 7 раскладок
3)  *dictr.py* - централизованный словарь *data_dict* с конфигурацией всех раскладок
- <ins>**Система параллельной обработки:**</ins>
1)  *blocks.py* - функции *process_block_return()* и *merge_block_data()* для работы с блоками
2)  *parallel_large.py* - многопроцессорная обработка через *multiprocessing.Pool*
3)  *parallel_large_rabbit.py* - распределенная обработка через *RabbitMQ*
4)  *worker_rabbit.py* - воркер-процесс для очереди сообщений
- <ins>**Визуализация и отчетность:**</ins>
1)  *charts_bar.py* - горизонтальные гистограммы нагрузок на пальцы
2)  *charts_multi.py* - множественные графики по типам пальцев
3)  *charts_pie.py* - круговые диаграммы распределения по рукам
4)  *charts_summary.py* - сводная диаграмма общей нагрузки
5)  *visualmain.py* - агрегатор всех визуализаций
6)  *stats.py* - утилиты для табличного вывода статистики
- <ins>**Хранилище и инфраструктура:**</ins>
1)  *storage.py* - класс *RedisStorage* для работы с Redis
2)  *main.py* - главный модуль запуска анализа
3)  *utils.py* - вспомогательные функции (импортируются в других модулях)
- <ins>**Тестирование:**</ins>
1)  *test_keyboard_analyzer.py* - тесты анализатора
2)  *test_keyboard_layout.py* - тесты раскладок
3)  *test_utils_stats.py* - тесты утилит статистики
4)  *test_integration.py* - интеграционные тесты Redis

### Metrics and data processing

Распределение пальцев:

    Левая рука: мизинец (f5l), безымянный (f4l), средний (f3l), указательный (f2l), большой (f1l)
    Правая рука: большой (f1r), указательный (f2r), средний (f3r), безымянный (f4r), мизинец (f5r)

Распределение по колонкам клавиатуры:

    1)  Колонки 0-1: f5l (мизинец левый)
    2)  Колонка 2: f4l (безымянный левый)
    3)  Колонка 3: f3l (средний левый)
    4)  Колонки 4-5: f2l (указательный левый)
    5)  Колонки 6-7: f2r (указательный правый)
    6)  Колонка 8: f3r (средний правый)
    7)  Колонка 9: f4r (безымянный правый)
    8)  Колонки 10-12: f5r (мизинец правый)

<ins>Система штрафных баллов:</ins>
1)  **0 баллов**: та же клавиша
2)  **1 балл**: вертикальные/горизонтальные перемещения на 1 позицию
3)  **2 балла**: диагональные перемещения (разница по обеим осям = 1)
4)  **3-4 балла**: сложные перемещения (разница ≥2 по любой оси)

<ins>Учет особенностей раскладок:</ins>

- **Раскладка "Вызов":**
1)  Дополнительный штраф +4 за использование вторых символов на клавишах
2)  Специальная обработка многосимвольных клавиш в get_coords()
- **Дифференциация по рядам:**
1)  Ряд 2 ("домашний") - минимальные штрафы
2)  Ряды 1 и 3 - повышенные штрафы
3)  Ряд 0 (верхний) - максимальные штрафы
- **Учет эргономики:**
1)  Вертикальные перемещения в центральных колонках (5-6) - сниженные штрафы
2)  Крайние колонки (0, 12) - повышенные штрафы
3)  Горизонтальные перемещения к мизинцам - дополнительные штрафы

<ins>Дополнительные факторы:</ins>

- **Пробелы:**
  - Распределение между большими пальцами по разным схемам для каждой раскладки
  - Учет переходов между руками
- **Заглавные буквы:**
  - Штраф +2 за каждую заглавную букву
  - Нагрузка на левый мизинец (клавиша Shift)
- **Переходы между руками:**
  - Подсчет смены активной руки
  - Учет в общей эргономической оценке
- **Учет знаков препинания в анализе**

<ins>Процесс обработки:</ins>

1)  Разбиение текста на блоки по 50,000 символов
2)  Параллельная обработка через Pool процессов или RabbitMQ воркеры
3)  Накопление результатов в основном анализаторе через merge_block_data()
4)  Детальный анализ перемещений для последнего блока
5)  Сохранение результатов в Redis и генерация визуализаций
6)  Вывод сравнительных отчетов в консоль

### Results and its practical relevance

<ins>Система генерирует комплексные отчеты:</ins>
 
- **Детальный анализ перемещений (*analyze_movement_details()*)**
  - Первые 20-50 переходов между символами
  - Координаты, типы перемещений, штрафы для каждой раскладки
  - Использование дублирующих символов (для раскладки "Вызов")
- **Статистика нагрузок (*print_final_results()*, *print_press_statistics()*)**
  - Нагрузка на каждый палец для всех раскладок
  - Общее количество нажатий
  - Сравнительная таблица эффективности
- **Визуальные отчеты (4 типа графиков)**
  - Горизонтальные гистограммы нагрузок на пальцы
  - Круговые диаграммы распределения по рукам
  - Множественные графики по типам пальцев
  - Сводная диаграмма общей нагрузки
- **Данные для хранения**
  - Результаты сохраняются в Redis по ключу "layouts"
  - Визуализации сохраняются в */app/data_output/*


<ins>Практическая значимость</ins>

- **Для разработчиков раскладок:**
  - Инструмент для объективной оценки новых разработок
  - Возможность итеративного улучшения на основе количественных данных
  - Сравнение с существующими решениями
- **Для пользователей:**
  - Обоснованный выбор раскладки под индивидуальные потребности
  - Понимание компромиссов каждой раскладки
  - Возможность адаптации под специфические задачи (программирование, писательство и т.д.)
- **Для исследований эргономики:**
  - Методология может быть расширена для других языков
  - Адаптируемая система оценки под разные критерии
  - Открытая архитектура для дальнейших улучшений
- **Результаты анализа позволяют:**
  - Объективно сравнить эргономичность разных раскладок
  - Выявить слабые места каждой раскладки
  - Оптимизировать раскладку под конкретные паттерны печати
  - Принять обоснованное решение о выборе раскладки


<ins>Ограничения и перспективы</ins>
- **Текущие ограничения:**
  - Анализ основан на статических текстовых корпусах
  - Не учитывает индивидуальные особенности печати
  - Ограниченный набор сравниваемых раскладок
- **Возможности расширения:**
  - Интеграция с системами анализа живого ввода
  - Учет биомеханических особенностей рук
  - Поддержка дополнительных раскладок и языков
  - ML-алгоритмы для оптимизации раскладок