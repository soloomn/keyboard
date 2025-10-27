from models import LayoutAnalyzer
from utils import show_finger_stats, analyze_large_file
#from visual import show_all
import json

if __name__ == "__main__":
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

    layout_name = "qwer"

    print(f"\nСтатистика по выбранной раскладке {layout_name}:")
    df = show_finger_stats(analyzer, layout_name)

    data = analyzer.reverser
    with open("/app/data_output/layouts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Анализ завершен, данные сохранены в /app/data_output/layouts.json")

    #show_all(data['diktor'], data['qwer'], data['vyzov'])
