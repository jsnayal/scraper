from enum import Enum


class RedisKeys(Enum):
    PRODUCT_CACHE = "product_cache"


class CacheType(Enum):
    REDIS = "redis"


class DatabaseType(Enum):
    JSON = "json"
    MYSQL = "mysql"


class NotificationType(Enum):
    CONSOLE = "console"
    MESSAGE = "message"
