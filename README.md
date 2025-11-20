<h1 align="center">KEYBOARD</h1>

<h6 align="center">
Transforming typing for a healthier, smarter future.
</h6>


<p align="center">
  <img src="https://img.shields.io/github/last-commit/soloomn/keyboard?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit" />
  <img src="https://img.shields.io/github/languages/top/soloomn/keyboard?style=flat&logo=python&logoColor=white&color=0080ff" alt="python" />
  <img src="https://img.shields.io/github/languages/count/soloomn/keyboard?style=flat&color=0080ff" alt="languages" />
  <img src="https://img.shields.io/github/v/tag/soloomn/keyboard.svg?label=Release&style=flat&color=0080ff" alt="release" />
</p>


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

<p align="center">
  <img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="docker" />
  <img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="python" />
  <img src="https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat&logo=Poetry&logoColor=white" alt="poetry" />
  <img src="https://img.shields.io/badge/Redis-FF4438.svg?style=flat&logo=Redis&logoColor=white" alt="redis" />
  <img src="https://img.shields.io/badge/RabbitMQ-FF6600.svg?style=flat&logo=RabbitMQ&logoColor=white" alt="rabbitmq" />
  <img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="numpy" />
  <img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas" />
  <img src="https://custom-icon-badges.demolab.com/badge/Matplotlib-71D291?logo=matplotlib&logoColor=fff" alt="matplotlib" />
  <img src="https://img.shields.io/badge/Rich-FAE742.svg?style=flat&logo=Rich&logoColor=black" alt="rich" />
  <img src="https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat&logo=Pytest&logoColor=white" alt="pytest" />
  <img src="https://img.shields.io/badge/Sphinx-000000.svg?style=flat&logo=Sphinx&logoColor=white)" alt="sphinx"/>
  <img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="markdown" />
  <img src="https://img.shields.io/badge/TOML-9C4121.svg?style=flat&logo=TOML&logoColor=white" alt="TOML" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white" alt="github actions" />
</p>

---

## Table of Contents

- [Overview](#overview)
  - [Case definition](#case-definition)
  - [Overall project description](#overall-project-description)
  - [Principal purpose](#principal-purpose)
  - [Key features](#key-features)
  - [Contex and actuality](#context-and-actuality)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)

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
- **Package Manager:** poetry (recommended) or pip
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

`keyboard` использует стандартный стек Python для тестирования (pytest / unittest).

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


