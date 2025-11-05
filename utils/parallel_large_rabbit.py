import json
import pika
import time
from models import RedisStorage, LayoutAnalyzer
from utils import merge_block_data

def send_blocks_to_workers(filename: str, chunk_size: int = 50000):
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


    # Подключаемся к RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq', 5672, credentials=pika.PlainCredentials('user', 'password'))
    )
    channel = connection.channel()
    channel.queue_declare(queue='analysis_tasks', durable=True)

    for i, block in enumerate(blocks):
        message = json.dumps({"id": i, "text": block})
        channel.basic_publish(
            exchange='',
            routing_key='analysis_tasks',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    connection.close()

    last_block_text = blocks[-1] if blocks else ''.join(buffer)
    storage = RedisStorage()
    storage.save("last_block", last_block_text)

    return len(blocks)

def analyze_large_file_rabbit(filename: str):
    analyzer = LayoutAnalyzer()
    storage = RedisStorage()
    total_blocks = send_blocks_to_workers(filename, chunk_size=50000)

    collected = 0
    while collected < total_blocks:
        keys = storage.client.keys("block_*")
        collected = len(keys)
        print(f"Собрано блоков: {collected}/{total_blocks}")
        time.sleep(1)

    for key in sorted(keys):
        block_data = storage.load(key)
        merge_block_data(analyzer, block_data)

    # Анализ перемещений для последнего блока
    last_block_text = storage.load("last_block")
    if last_block_text:
        movements_info = analyzer.analyze_movement_details(last_block_text)
        analyzer.print_detailed_analysis(movements_info)
    else:
        print("Не удалось получить последний блок для анализа перемещений")

    return analyzer