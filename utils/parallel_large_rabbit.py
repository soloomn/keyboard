import json
import pika
import time
from models import RedisStorage, LayoutAnalyzer
from utils import merge_block_data

storage = RedisStorage()

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
    channel.queue_declare(queue='results', durable=True)

    for i, block in enumerate(blocks):
        message = json.dumps({"id": i, "text": block})
        channel.basic_publish(
            exchange='',
            routing_key='analysis_tasks',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    print(f"✓ Отправлено {len(blocks)} блоков в обработку")

    last_block_text = blocks[-1] if blocks else ''.join(buffer)

    storage.save("last_block", last_block_text)
    storage.save("blocks_len", len(blocks))

    return connection


def wait_for_completion(connection, timeout=300):
    """Ждет завершения всех блоков через RabbitMQ results очередь"""
    total_blocks = storage.load("blocks_len")
    channel = connection.channel()

    completed_blocks = set()
    start_time = time.time()

    def results_callback(ch, method, properties, body):
        data = json.loads(body)
        block_id = data["block_id"]
        completed_blocks.add(block_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f" - Получено подтверждение блока {block_id} ({len(completed_blocks)}/{total_blocks})")

    channel.basic_consume(queue='results', on_message_callback=results_callback)

    print("Ожидаем завершения обработки...")

    # Обрабатываем сообщения о завершении
    while len(completed_blocks) < total_blocks:
        if time.time() - start_time > timeout:
            print(f"Таймаут! Завершено {len(completed_blocks)}/{total_blocks}")
            break

        connection.process_data_events(time_limit=1)  # Обрабатываем сообщения 1 секунду

    connection.close()
    print("Все блоки обработаны!")


def analyze_large_file_rabbit(filename: str):
    analyzer = LayoutAnalyzer()
    # Отправляем блоки и получаем соединение для отслеживания
    connection = send_blocks_to_workers(filename, chunk_size=50000)

    # Ждем завершения через RabbitMQ
    wait_for_completion(connection)

    # Собираем результаты из Redis
    keys = storage.client.keys("block_*")
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
