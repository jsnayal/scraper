import redis
import hashlib
from abc import ABC, abstractmethod
from scraper.constants import RedisKeys


class Cache(ABC):
    """
    Abstract base class for cache implementations
    This class defines the interface for caching strategies, including methods
    for checking if a product is cached and for caching a product.
    """
    @abstractmethod
    def is_cached(self, product):
        """
        Check if a product is cached
        :param product: product to be checked
        :return: None
        """
        NotImplementedError()

    @abstractmethod
    def cache_product(self, product):
        """
        Cache a product instance
        :param product: product to be cached
        :return: None
        """
        NotImplementedError()


class RedisCache(Cache):
    """
    Concrete implementation of the Cache interface using Redis.
    This class uses Redis to cache product data and check if a product is cached.
    """
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def is_cached(self, product) -> bool:
        """
        Check if a product price is cached in Redis
        :param product: product whose price is to be checked
        :return: True if the product is cached and the price matches, False otherwise
        """
        key = hashlib.md5(product["product_title"].encode()).hexdigest()
        product_price = self.client.hget(RedisKeys.PRODUCT_CACHE.value, key)
        return True if product_price and float(product_price) == product['product_price'] else False

    def cache_product(self, product) -> None:
        """
        Cache a product in Redis
        :param product: product whose price is to be cached
        :return: None
        """
        key = hashlib.md5(product["product_title"].encode()).hexdigest()
        self.client.hset(RedisKeys.PRODUCT_CACHE.value, key, product["product_price"])
