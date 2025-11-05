"""
Модуль воркера для распределенной обработки текстовых блоков через RabbitMQ.

Содержит worker-процесс, который получает задания из очереди RabbitMQ,
обрабатывает текстовые блоки и сохраняет результаты в Redis с отправкой
подтверждений о завершении обработки.

Основные возможности:
- Получение текстовых блоков из очереди analysis_tasks
- Обработка блоков с помощью process_block_return
- Сохранение результатов в Redis
- Отправка подтверждений в очередь results
- Автоматическое подтверждение обработки сообщений

Используемые технологии:
- RabbitMQ для распределенной обработки заданий
- Redis для хранения промежуточных результатов
- JSON для сериализации данных
"""

import pika
import json
import time
from utils import process_block_return
from models import RedisStorage


def main():
    """
    Основная функция воркера для обработки текстовых блоков.

    ВХОД: Нет

    ВЫХОД:
        None (работает в бесконечном цикле до получения сигнала завершения)

    Действия функции:
        - Подключается к RabbitMQ и Redis
        - Объявляет необходимые очереди
        - Начинает прослушивание очереди analysis_tasks
        - Обрабатывает каждый полученный блок
        - Сохраняет результаты в Redis
        - Отправляет подтверждения в очередь results
    """
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
        """
        Callback-функция для обработки сообщений из очереди analysis_tasks.

        ВХОД:
            ch: Канал RabbitMQ
            method: Метод доставки
            properties: Свойства сообщения
            body: Тело сообщения с данными блока

        ВЫХОД:
            None
        """
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