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

from utils import show_finger_stats, analyze_large_file_rabbit, analyze_large_file_parallel_merge
from models import RedisStorage

if __name__ == "__main__":
    """
    Главная функция программы для анализа эргономики клавиатурных раскладок.

    ВХОД: Нет (использует файл 'voina-i-mir.txt' для анализа)

    ВЫХОД: Нет (выводит результаты анализа в консоль и графики)
    """
    # Основной анализ

    print("Анализируем 'Войну и мир' по частям...")

    use_rabbit = True
    if use_rabbit:
        analyzer = analyze_large_file_rabbit("voina-i-mir.txt")
    else:
        analyzer = analyze_large_file_parallel_merge("voina-i-mir.txt", chunk_size=50000)


    # Детальный анализ перемещений
    print("Детальный анализ перемещений...")
    analyzer.print_final_results()

    analyzer.print_press_statistics()

    analyzer.print_comparative_analysis()

    layout_name = "qwer"

    print(f"\nСтатистика по выбранной раскладке {layout_name}:")
    df = show_finger_stats(analyzer, layout_name)

    data = analyzer.reverser
    storage = RedisStorage()

    storage.save("layouts", data)
    #with open("/app/data_output/layouts.json", "w", encoding="utf-8") as f:
        #json.dump(data, f, ensure_ascii=False, indent=2)

    #print("Анализ завершен, данные сохранены в /app/data_output/layouts.json")

