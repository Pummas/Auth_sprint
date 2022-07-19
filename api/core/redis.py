from abc import ABC, abstractmethod
import json


class CacheStorage(ABC):
    @abstractmethod
    def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    def set(self, key: str, value: str, expire: int, **kwargs):
        pass

    @abstractmethod
    def remove(self, key: str):
        pass


class RedisStorage(CacheStorage):
    def __init__(self, redis_adapter):
        self.redis = redis_adapter

    def get(self, key: str, **kwargs):
        data = self.redis.get(key)
        if data is None:
            return
        else:
            return json.loads(data)

    def set(self, key: str, value: str, expire: int, **kwargs):
        self.redis.set(key, json.dumps(value), expire)

    def remove(self, key: str):
        self.redis.delete(key)
