import json
import pytest
from unittest.mock import MagicMock
from models.storage import RedisStorage


@pytest.fixture
def storage():
    s = RedisStorage()
    s.client = MagicMock()
    return s


def test_save_calls_redis_set(storage):
    storage.save("key1", {"a": 1})
    storage.client.set.assert_called_once()
    saved_key, saved_value = storage.client.set.call_args[0]
    assert saved_key == "key1"
    assert json.loads(saved_value) == {"a": 1}


def test_load_returns_none_when_no_key(storage):
    storage.client.get.return_value = None
    result = storage.load("missing")
    assert result is None


def test_load_returns_parsed_json(storage):
    storage.client.get.return_value = json.dumps({"x": 10})
    result = storage.load("exists")
    assert result == {"x": 10}
