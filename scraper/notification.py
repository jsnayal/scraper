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


class Subscriber:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def notify(self, data, notification: Notification):
        message = f"{self.name} is notified\n{data}"
        notification.notify(message)


class Publisher:
    def __init__(self, notification: Notification):
        self.subscribers = []
        self.notification = notification

    def subscribe(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    def publish(self, data):
        for subscriber in self.subscribers:
            subscriber.notify(data, self.notification)


class MessagePublisher:
    publisher: Publisher = None

    @classmethod
    def get_publisher(cls):
        return cls.publisher

    @classmethod
    def set_publisher(cls, publisher):
        if cls.publisher is None:
            cls.publisher = publisher
