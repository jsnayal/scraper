import redis
import hashlib

from scraper.constants import RedisKeys


class Cache:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def is_cached(self, product):
        key = hashlib.md5(product["title"].encode()).hexdigest()
        return True if self.client.hget(RedisKeys.PRODUCT_CACHE.value, key) else False

    def cache_product(self, product):
        key = hashlib.md5(product["title"].encode()).hexdigest()
        self.client.hset(RedisKeys.PRODUCT_CACHE.value, key, product["price"])
