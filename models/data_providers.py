"""
Провайдеры текста и блоков текста для анализа.

Абстрагируют источник данных (файлы, Redis и т.п.) от анализатора.

Содержит два основных типа провайдеров:
- TextProvider: предоставляет полный текст в виде одной строки
- BlockProvider: предоставляет текст по блокам фиксированного размера

Используется для:
- Загрузки текстовых данных из различных источников
- Подготовки данных для анализа клавиатурных раскладок
- Потоковой обработки больших текстовых файлов
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from models import RedisStorage


class TextProvider(ABC):
    """
    Абстрактный источник полного текста для анализа.

    ВХОД: Нет (определяется конкретной реализацией)
    ВЫХОД: Полный текст в виде строки
    """

    @abstractmethod
    def get_text(self) -> str:
        """
        Вернуть весь текст в виде одной строки.

        ВХОД: Нет
        ВЫХОД: str - полный текст
        """
        raise NotImplementedError


class FileTextProvider(TextProvider):
    """
    Источник текста из одного файла.

    ВХОД: path - путь к файлу, encoding - кодировка файла
    ВЫХОД: str - содержимое файла
    """

    def __init__(self, path: str, encoding: str = "utf-8") -> None:
        """
        Инициализация провайдера файла.

        ВХОД:
            path: str - путь к файлу
            encoding: str - кодировка файла (по умолчанию "utf-8")
        ВЫХОД: None
        """
        self.path = path
        self.encoding = encoding

    def get_text(self) -> str:
        """
        Чтение всего содержимого файла.

        ВХОД: Нет
        ВЫХОД: str - содержимое файла в виде строки
        """
        with open(self.path, "r", encoding=self.encoding) as f:
            return f.read()


class MultiFileTextProvider(TextProvider):
    """
    Источник текста из нескольких файлов (конкатенация).

    ВХОД: paths - список путей к файлам, encoding - кодировка файлов
    ВЫХОД: str - объединенное содержимое всех файлов
    """

    def __init__(self, paths: List[str], encoding: str = "utf-8") -> None:
        """
        Инициализация провайдера нескольких файлов.

        ВХОД:
            paths: List[str] - список путей к файлам
            encoding: str - кодировка файлов (по умолчанию "utf-8")
        ВЫХОД: None
        """
        self.paths = paths
        self.encoding = encoding

    def get_text(self) -> str:
        """
        Чтение и объединение содержимого нескольких файлов.

        ВХОД: Нет
        ВЫХОД: str - объединенное содержимое всех файлов, разделенное переводом строки
        """
        parts: List[str] = []
        for path in self.paths:
            with open(path, "r", encoding=self.encoding) as f:
                parts.append(f.read())
        return "\n".join(parts)


class RedisTextProvider(TextProvider):
    """
    Источник текста из Redis по ключу.

    ВХОД: key - ключ в Redis, storage - экземпляр RedisStorage
    ВЫХОД: str - текст из Redis
    """

    def __init__(
        self,
        key: str,
        storage: Optional[RedisStorage] = None,) -> None:
        """
        Инициализация Redis провайдера.

        ВХОД:
            key: str - ключ для получения текста из Redis
            storage: Optional[RedisStorage] - экземпляр хранилища (по умолчанию создается новый)
        ВЫХОД: None
        """
        self.key = key
        self.storage = storage or RedisStorage()

    def get_text(self) -> str:
        """
        Получение текста из Redis по ключу.

        ВХОД: Нет
        ВЫХОД: str - текст из Redis
        Исключения: TypeError - если данные по ключу не являются строкой
        """
        data = self.storage.load(self.key)
        if not isinstance(data, str):
            raise TypeError(f"Redis key {self.key!r} does not contain plain text")
        return data


class BlockProvider(ABC):
    """
    Абстрактный источник блоков текста фиксированного/ограниченного размера.

    ВХОД: Нет (определяется конкретной реализацией)
    ВЫХОД: Итератор строк (блоков текста)
    """

    @abstractmethod
    def iter_blocks(self) -> Iterable[str]:
        """
        Итерироваться по блокам текста.

        ВХОД: Нет
        ВЫХОД: Iterable[str] - итератор по блокам текста
        """
        raise NotImplementedError


class FileBlockProvider(BlockProvider):
    """
    Читает файл построчно и отдаёт блоки примерно по chunk_size символов.

    ВХОД: path - путь к файлу, chunk_size - размер блока, encoding - кодировка
    ВЫХОД: Итератор блоков текста
    """

    def __init__(self, path: str, chunk_size: int = 50_000, encoding: str = "utf-8") -> None:
        """
        Инициализация провайдера блоков из файла.

        ВХОД:
            path: str - путь к файлу
            chunk_size: int - размер блока в символах (по умолчанию 50000)
            encoding: str - кодировка файла (по умолчанию "utf-8")
        ВЫХОД: None
        """
        self.path = path
        self.chunk_size = chunk_size
        self.encoding = encoding

    def iter_blocks(self) -> Iterable[str]:
        """
        Чтение файла блоками фиксированного размера.

        ВХОД: Нет
        ВЫХОД: Iterable[str] - итератор по блокам текста
        """
        buffer: List[str] = []
        buffer_len = 0

        with open(self.path, "r", encoding=self.encoding) as f:
            for line in f:
                buffer.append(line)
                buffer_len += len(line)

                if buffer_len >= self.chunk_size:
                    yield "".join(buffer)
                    buffer.clear()
                    buffer_len = 0

        if buffer:
            # остаток
            yield "".join(buffer)


class MultiFileBlockProvider(BlockProvider):
    """
    Блоки по нескольким файлам подряд (как один большой текст).

    ВХОД: paths - список путей к файлам, chunk_size - размер блока, encoding - кодировка
    ВЫХОД: Итератор блоков текста
    """

    def __init__(self, paths: List[str], chunk_size: int = 50_000, encoding: str = "utf-8") -> None:
        """
        Инициализация провайдера блоков из нескольких файлов.

        ВХОД:
            paths: List[str] - список путей к файлам
            chunk_size: int - размер блока в символах (по умолчанию 50000)
            encoding: str - кодировка файлов (по умолчанию "utf-8")
        ВЫХОД: None
        """
        self.paths = paths
        self.chunk_size = chunk_size
        self.encoding = encoding

    def iter_blocks(self) -> Iterable[str]:
        """
        Чтение нескольких файлов блоками фиксированного размера.

        ВХОД: Нет
        ВЫХОД: Iterable[str] - итератор по блокам текста из всех файлов
        """
        buffer: List[str] = []
        buffer_len = 0

        for path in self.paths:
            with open(path, "r", encoding=self.encoding) as f:
                for line in f:
                    buffer.append(line)
                    buffer_len += len(line)

                    if buffer_len >= self.chunk_size:
                        yield "".join(buffer)
                        buffer.clear()
                        buffer_len = 0

        if buffer:
            yield "".join(buffer)

