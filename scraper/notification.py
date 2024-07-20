import redis
import hashlib
from abc import ABC, abstractmethod
from scraper.constants import RedisKeys


class Notification(ABC):
    @abstractmethod
    def notify(self, message):
        NotImplementedError()


class ConsoleNotification(Notification):
    def notify(self, message):
        print(message)

