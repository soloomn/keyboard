"""
Основной модуль для запуска анализа клавиатурных раскладок.

Содержит главную функцию программы, которая координирует процесс анализа:
- Загрузка и обработка текстовых данных
- Анализ эргономики раскладок
- Визуализация результатов
- Вывод статистики

Использует модули:
- models: для анализа раскладок и работы с Redis
- utils: для работы с большими файлами и статистикой
- visual: для графического представления результатов

Основной функционал:
- Анализ больших текстовых файлов (например, "Война и мир")
- Сравнение 7 русскоязычных клавиатурных раскладок
- Сохранение результатов в Redis и вывод статистики
"""

from utils import show_finger_stats, analyze_large_file_rabbit, analyze_large_file_parallel_merge
from models import RedisStorage

if __name__ == "__main__":
    """
    Главная функция программы для анализа эргономики клавиатурных раскладок.

    ВХОД: 
        Нет (использует файл 'voina-i-mir.txt' для анализа)

    ВЫХОД: 
        None

    Действия функции:
        - Загружает и анализирует текст "Война и мир" по частям
        - Сравнивает эргономику 7 клавиатурных раскладок
        - Выводит финальные результаты, статистику нажатий и сравнительный анализ
        - Сохраняет данные в Redis для дальнейшего использования
        - Отображает статистику по выбранной раскладке

    Используемые файлы:
        - 'voina-i-mir.txt' - исходный текст для анализа

    Используемые модули:
        - utils: для анализа больших файлов и отображения статистики
        - models: для работы с хранилищем Redis
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

    # Анализ последовательностей
    print("\nАнализ пальцевых переборов...")
    if hasattr(analyzer, 'sequence_stats_accumulated'):
        analyzer.print_sequence_analysis(analyzer.sequence_stats_accumulated)
    else:
        # Если нет накопленных данных, анализируем последний блок
        last_block_text = storage.load("last_block")
        if last_block_text:
            sequence_stats = analyzer.analyze_sequences(last_block_text)
            analyzer.print_sequence_analysis(sequence_stats)

            # Детальные примеры
            examples = analyzer.analyze_sequences_detailed(last_block_text)
            analyzer.print_detailed_sequences(examples)

    # Сохраняем данные последовательностей
    if hasattr(analyzer, 'sequence_stats_accumulated'):
        storage.save("sequence_stats", analyzer.sequence_stats_accumulated)

    storage.save("layouts", data)


    #with open("/app/data_output/layouts.json", "w", encoding="utf-8") as f:
        #json.dump(data, f, ensure_ascii=False, indent=2)

    #print("Анализ завершен, данные сохранены в /app/data_output/layouts.json")

