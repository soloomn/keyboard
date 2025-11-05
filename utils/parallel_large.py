from multiprocessing import Pool
from models import LayoutAnalyzer
from utils import merge_block_data, process_block_return

def analyze_large_file_parallel_merge(filename: str, chunk_size: int = 50000, n_processes: int = 4) -> LayoutAnalyzer:
    # Разбиваем текст на блоки
    blocks = []
    buffer = []
    buffer_len = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            buffer.append(line)
            buffer_len += len(line)
            if buffer_len >= chunk_size:
                blocks.append(''.join(buffer))
                buffer.clear()
                buffer_len = 0
        if buffer:
            blocks.append(''.join(buffer))

    # Параллельно обрабатываем блоки
    with Pool(n_processes) as pool:
        blocks_data = pool.map(process_block_return, blocks)

    # Создаем основной analyzer и аккумулируем данные
    main_analyzer = LayoutAnalyzer()
    for block_data in blocks_data:
        merge_block_data(main_analyzer, block_data)

    movements_info = main_analyzer.analyze_movement_details(''.join(buffer))
    main_analyzer.print_detailed_analysis(movements_info)
    return main_analyzer