import pika
import json
from utils import process_block_return
from models import RedisStorage

redis = RedisStorage()

def callback(ch, method, properties, body):
    data = json.loads(body)
    block_id = data["id"]
    block_text = data["text"]

    # Обработка блока
    result = process_block_return(block_text)

    # Сохраняем результат в Redis
    redis.save(f"block_{block_id}", result)

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(
    pika.ConnectionParameters('rabbitmq', 5672, credentials=pika.PlainCredentials('user', 'password'))
)

channel = connection.channel()
channel.queue_declare(queue='analysis_tasks', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='analysis_tasks', on_message_callback=callback)
channel.start_consuming()