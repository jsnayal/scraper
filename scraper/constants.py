from enum import Enum


class RedisKeys(Enum):
    """
    Enumeration for Redis keys used in caching
    """
    PRODUCT_CACHE = "product_cache"


class CacheType(Enum):
    """
    Enumeration for different types of cache implementations
    """
    REDIS = "redis"


class DatabaseType(Enum):
    """
    Enumeration for different types of database implementations
    """
    JSON = "json"
    MYSQL = "mysql"


class NotificationType(Enum):
    """
    Enumeration for different types of notification strategies
    """
    CONSOLE = "console"
    MESSAGE = "message"


# Static authentication token used for securing endpoints.
STATIC_AUTH_TOKEN = "1dcd0f4088ab3aceb790bc4077f2581f"
# Number of seconds to wait before retrying a failed operation
RETRY_SECONDS = 5
# Number of retry attempts for a failed operation
RETRY_COUNT = 3


