import pika
import json
import time
from utils import process_block_return
from models import RedisStorage


def main():
    storage = RedisStorage()
    blocks_len = storage.load("blocks_len")

    # Подключаемся к RabbitMQ для получения заданий
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq', 5672, credentials=pika.PlainCredentials('user', 'password'))
    )
    channel = connection.channel()

    # Объявляем обе очереди
    channel.queue_declare(queue='analysis_tasks', durable=True)
    channel.queue_declare(queue='results', durable=True)
    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        block_id = data["id"]
        block_text = data["text"]

        try:
            print(f"Обрабатываю блок {block_id}...")

            # Обработка блока
            result = process_block_return(block_text)

            # Сохраняем в Redis
            storage.save(f"block_{block_id}", result)

            # Отправляем подтверждение в очередь results
            completion_msg = json.dumps({
                "block_id": block_id,
                "status": "completed",
                "timestamp": time.time()
            })

            channel.basic_publish(
                exchange='',
                routing_key='results',
                body=completion_msg,
                properties=pika.BasicProperties(delivery_mode=2)
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"Блок {block_id} обработан и подтвержден")

            if block_id >= (blocks_len-8):
                time.sleep(10)
                connection.close()
        except Exception as e:
            print(f"Ошибка в блоке {block_id}: {e}")

    # Начинаем слушать задания
    print("Worker запущен и ожидает сообщения...")
    channel.basic_consume(queue='analysis_tasks', on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    main()