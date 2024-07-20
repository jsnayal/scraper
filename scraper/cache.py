import redis
import hashlib
from abc import ABC, abstractmethod
from scraper.constants import RedisKeys


class Cache(ABC):
    @abstractmethod
    def is_cached(self, product):
        NotImplementedError()

    @abstractmethod
    def cache_product(self, product):
        NotImplementedError()


class RedisCache(Cache):
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def is_cached(self, product) -> bool:
        key = hashlib.md5(product["product_title"].encode()).hexdigest()
        product_price = self.client.hget(RedisKeys.PRODUCT_CACHE.value, key)
        return True if product_price and float(product_price) == product['product_price'] else False

    def cache_product(self, product) -> None:
        key = hashlib.md5(product["product_title"].encode()).hexdigest()
        self.client.hset(RedisKeys.PRODUCT_CACHE.value, key, product["product_price"])
