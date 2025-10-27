"""
Модуль для обработки больших текстовых файлов.

Содержит функцию analyze_large_file для анализа объемных текстовых данных
(например, книг) по частям без загрузки всего файла в оперативную память.
"""

def analyze_large_file(filename: str, analyzer, chunk_size: int = 50000) -> None:
    """
    Выполняет анализ большого текстового файла по частям.

    Это позволяет обрабатывать огромные тексты (например, "Войну и мир")
    без загрузки всего файла в память.

    ВХОД:
        filename (str): Путь к текстовому файлу для анализа
        analyzer (LayoutAnalyzer): Объект анализатора раскладок с методом analyze_text
        chunk_size (int, optional): Максимальный размер блока текста в символах для обработки за раз (по умолчанию 50000)

    ВЫХОД: Нет (результаты сохраняются во внутреннем состоянии анализатора и выводятся в консоль)
    """
    with open(filename, 'r', encoding='utf-8') as f:
        buffer = []
        buffer_len = 0
        for line in f:
            buffer.append(line)
            buffer_len += len(line)
            if buffer_len >= chunk_size:
                analyzer.analyze_text(''.join(buffer))
                buffer.clear()
                buffer_len = 0
        # анализируем остаток
        if buffer:
            analyzer.analyze_text(''.join(buffer))

        # Вывод результатов
        print("Детальный анализ перемещений...")
        movements_info = analyzer.analyze_movement_details(''.join(buffer))
        analyzer.print_detailed_analysis(movements_info)