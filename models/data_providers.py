"""
Провайдеры текста и блоков текста для анализа.

Абстрагируют источник данных (файлы, Redis и т.п.) от анализатора.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from models import RedisStorage


class TextProvider(ABC):
    """Абстрактный источник полного текста для анализа."""

    @abstractmethod
    def get_text(self) -> str:
        """Вернуть весь текст в виде одной строки."""
        raise NotImplementedError


class FileTextProvider(TextProvider):
    """Источник текста из одного файла."""

    def __init__(self, path: str, encoding: str = "utf-8") -> None:
        self.path = path
        self.encoding = encoding

    def get_text(self) -> str:
        with open(self.path, "r", encoding=self.encoding) as f:
            return f.read()


class MultiFileTextProvider(TextProvider):
    """Источник текста из нескольких файлов (конкатенация)."""

    def __init__(self, paths: List[str], encoding: str = "utf-8") -> None:
        self.paths = paths
        self.encoding = encoding

    def get_text(self) -> str:
        parts: List[str] = []
        for path in self.paths:
            with open(path, "r", encoding=self.encoding) as f:
                parts.append(f.read())
        return "\n".join(parts)


class RedisTextProvider(TextProvider):
    """Источник текста из Redis по ключу."""

    def __init__(
        self,
        key: str,
        storage: Optional[RedisStorage] = None,
    ) -> None:
        self.key = key
        self.storage = storage or RedisStorage()

    def get_text(self) -> str:
        data = self.storage.load(self.key)
        if not isinstance(data, str):
            raise TypeError(f"Redis key {self.key!r} does not contain plain text")
        return data


class BlockProvider(ABC):
    """Абстрактный источник блоков текста фиксированного/ограниченного размера."""

    @abstractmethod
    def iter_blocks(self) -> Iterable[str]:
        """Итерироваться по блокам текста."""
        raise NotImplementedError


class FileBlockProvider(BlockProvider):
    """Читает файл построчно и отдаёт блоки примерно по chunk_size символов."""

    def __init__(self, path: str, chunk_size: int = 50_000, encoding: str = "utf-8") -> None:
        self.path = path
        self.chunk_size = chunk_size
        self.encoding = encoding

    def iter_blocks(self) -> Iterable[str]:
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


# data_providers.py

class MultiFileBlockProvider(BlockProvider):
    """Блоки по нескольким файлам подряд (как один большой текст)."""

    def __init__(self, paths: List[str], chunk_size: int = 50_000, encoding: str = "utf-8") -> None:
        self.paths = paths
        self.chunk_size = chunk_size
        self.encoding = encoding

    def iter_blocks(self) -> Iterable[str]:
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

