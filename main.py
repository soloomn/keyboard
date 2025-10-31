"""
Основной модуль для запуска анализа клавиатурных раскладок.

Содержит главную функцию программы, которая координирует процесс анализа:
- Загрузка и обработка текстовых данных
- Анализ эргономики раскладок
- Визуализация результатов
- Вывод статистики

Использует модули:
- models: для анализа раскладок
- utils: для работы с большими файлами и статистикой
- visual: для графического представления результатов
"""

from models import LayoutAnalyzer
from utils import show_finger_stats, analyze_large_file
#from visual import show_all
import json

if __name__ == "__main__":
    """
    Главная функция программы для анализа эргономики клавиатурных раскладок.

    ВХОД: Нет (использует файл 'voina-i-mir.txt' для анализа)

    ВЫХОД: Нет (выводит результаты анализа в консоль и графики)
    """
    # Основной анализ
    analyzer = LayoutAnalyzer()

    print("Анализируем 'Войну и мир' по частям...")
    analyze_large_file("voina-i-mir.txt", analyzer, chunk_size=50000)

    #with open('voina-i-mir.txt', 'r', encoding='utf-8') as f:
    #text = f.read()

    # Анализ текста
    #print("Запуск анализа...")
    #analyzer.analyze_text(text)

    # Детальный анализ перемещений
    print("Детальный анализ перемещений...")
    #movements_info = analyzer.analyze_movement_details(text)
    #analyzer.print_detailed_analysis(movements_info)
    analyzer.print_final_results()

    analyzer.print_press_statistics()

    analyzer.print_comparative_analysis()

    layout_name = "qwer"

    print(f"\nСтатистика по выбранной раскладке {layout_name}:")
    df = show_finger_stats(analyzer, layout_name)

    data = analyzer.reverser
    with open("/app/data_output/layouts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Анализ завершен, данные сохранены в /app/data_output/layouts.json")

    #show_all(data['diktor'], data['qwer'], data['vyzov'], data["ant"], data["skoropis"], data["rusphone"], data["zubachew"])
