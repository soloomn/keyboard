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
import time
from utils import show_finger_stats, analyze_large_file_rabbit
from models import RedisStorage

storage = RedisStorage()

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

    CONTROL_KEY = "control:start_analysis"
    FILENAMES_KEY = "control:filenames"
    JOB_ID_KEY = "control:current_job_id"
    DATA_KEY = "control:metrics"

    print("Ожидаем разрешения на запуск анализа от FastAPI (Redis флаг)...")

    while True:
        val = storage.load(CONTROL_KEY)
        if val == "ready":
            metrics = storage.load(FILENAMES_KEY)
            print("Получен сигнал 'ready' — запускаем анализ.")
            break
        time.sleep(1)

    print(metrics)

    # сразу сбрасываем флаг, чтобы не стартовать повторно
    storage.save(CONTROL_KEY, "blocked")

    job_id = storage.load(JOB_ID_KEY)

    filenames = storage.load(FILENAMES_KEY)

    print(f"Анализируем {filenames} по частям...")

    if job_id:
        storage.save(f"job:{job_id}:status", "running")

    try:

        # Запускаем анализ
        analyzer = analyze_large_file_rabbit(filenames)

        print("Детальный анализ перемещений...")

        analyzer.print_final_results()

        analyzer.print_press_statistics()

        analyzer.print_comparative_analysis()

        layout_name = "qwer"

        df = show_finger_stats(analyzer, layout_name, output_file="/app/data_output/output.txt")

        # Анализ последовательностей
        print("\nАнализ пальцевых переборов...")
        analyzer.print_sequence_analysis()

        data_fingers = analyzer.reverser
        data_sequences = analyzer.stats_reverser

        storage.save("analysis:status", "finished")
        storage.save("layouts", data_fingers)
        storage.save("sequences", data_sequences)

        print("Анализ завершён!")

        # ставим статус "finished"
        if job_id:
            storage.save(f"job:{job_id}:status", "finished")

    except Exception as e:
        print(f"Ошибка анализа: {e}")
        # ставим статус "error"
        if job_id:
            storage.save(f"job:{job_id}:status", f"error:{e}")



