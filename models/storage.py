import os
import json
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379

class RedisStorage:
    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def save(self, key: str, data: dict | str | int):
        """Сохраняем данные (аналог записи в JSON-файл)."""
        self.client.set(key, json.dumps(data, ensure_ascii=False, indent=2))
        print(f"[Redis] saved key={key}")

    def load(self, key: str) -> dict | str | int |None:
        """Загружаем данные (аналог чтения JSON-файла)."""
        raw = self.client.get(key)
        if not raw:
            print(f"[Redis] no data for key={key}")
            return None
        else:
            print(f"[Redis] load key={key}")
            return json.loads(raw)