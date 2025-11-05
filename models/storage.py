"""
Модуль для работы с хранилищем данных Redis.

Предоставляет класс RedisStorage для сохранения и загрузки данных анализа
в распределенном хранилище Redis вместо локальных JSON-файлов.

Основные возможности:
- Сохранение данных анализа в Redis
- Загрузка данных из Redis
- Автоматическая сериализация/десериализация JSON
- Поддержка различных типов данных (dict, str, int)

Используемые технологии:
- Redis для распределенного хранения данных
- JSON для сериализации данных
- Environment variables для конфигурации подключения
"""

import os
import json
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379


class RedisStorage:
    """
    Класс для работы с хранилищем Redis.

    Обеспечивает сохранение и загрузку данных анализа в распределенном хранилище
    с автоматической сериализацией в формат JSON.

    Attributes:
        client: Клиент Redis для взаимодействия с сервером
    """
    def __init__(self):
        """
        Инициализация клиента Redis.

        ВХОД: Нет

        ВЫХОД:
            RedisStorage: Экземпляр класса для работы с Redis
        """
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def save(self, key: str, data: dict | str | int):
        """
        Сохраняет данные в Redis (аналог записи в JSON-файл).

        ВХОД:
            key (str): Ключ для сохранения данных
            data (dict | str | int): Данные для сохранения

        ВЫХОД:
            None

        Действия функции:
            - Сериализует данные в JSON формат
            - Сохраняет данные в Redis по указанному ключу
            - Выводит сообщение об успешном сохранении
        """
        self.client.set(key, json.dumps(data, ensure_ascii=False, indent=2))
        print(f"[Redis] saved key={key}")

    def load(self, key: str) -> dict | str | int | None:
        """
        Загружает данные из Redis (аналог чтения JSON-файла).

        ВХОД:
            key (str): Ключ для загрузки данных

        ВЫХОД:
            dict | str | int | None: Загруженные данные или None если ключ не найден

        Действия функции:
            - Пытается загрузить данные по указанному ключу
            - Десериализует данные из JSON формата
            - Возвращает данные или None если ключ не существует
            - Выводит сообщение о статусе операции
        """
        raw = self.client.get(key)
        if not raw:
            print(f"[Redis] no data for key={key}")
            return None
        else:
            print(f"[Redis] load key={key}")
            return json.loads(raw)
