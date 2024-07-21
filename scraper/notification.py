import redis
import hashlib
from abc import ABC, abstractmethod
from scraper.constants import RedisKeys


class Notification(ABC):
    """
    Abstract base class for notifications. This class defines the interface for any notification strategy
    """
    @abstractmethod
    def notify(self, message):
        """
        Sends a notification
        :param message: message to send
        Raises: NotImplementedError: If the method is not implemented by a subclass
        """
        NotImplementedError()


class ConsoleNotification(Notification):
    """
    Concrete implementation of the Notification interface for console output
    This class provides a method to print notification messages to the console
    """
    def notify(self, message):
        """
        Print the notification message to the console
        :param message: message to print
        :return: None
        """
        print(message)


class Subscriber:
    """
    Class representing a subscriber. Subscribers receive notifications from a Publisher
    """
    def __init__(self, name, email, phone):
        """
        Initialize the Subscriber instance.
        :param name: Name of the subscriber
        :param email: Email of the subscriber
        :param phone: Phone number of the subscriber
        """
        self.name = name
        self.email = email
        self.phone = phone

    def notify(self, data, notification: Notification):
        """
        Notify the subscriber with a given message
        :param data: data to be sent as message
        :param notification: The notification strategy to use
        :return:
        """
        message = f"{self.name} is notified\n{data}"
        notification.notify(message)


class Publisher:
    """
    Class representing a publisher. The Publisher maintains a list of subscribers and notifies them of new data
    """
    def __init__(self, notification: Notification):
        """
        Initialize the Publisher instance
        :param notification: The notification strategy to use
        """
        self.subscribers = []
        self.notification = notification

    def subscribe(self, subscriber: Subscriber):
        """
        Add a subscriber to the list
        :param subscriber: subscriber to add
        :return: None
        """
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber):
        """
        Remove a subscriber from the list
        :param subscriber: subscriber to remove
        :return: None
        """
        self.subscribers.remove(subscriber)

    def publish(self, data):
        """
        Notify all subscribers with the given data
        :param data: message to be sent to subscribers
        :return: None
        """
        for subscriber in self.subscribers:
            subscriber.notify(data, self.notification)


class MessagePublisher:
    """
    Singleton class for managing a global Publisher instance
    """
    publisher: Publisher = None

    @classmethod
    def get_publisher(cls):
        """
        Get the global publisher
        :return: global instance of publisher
        """
        return cls.publisher

    @classmethod
    def set_publisher(cls, publisher):
        """
        Set the global Publisher instance
        :param publisher: publisher to set
        :return: None
        """
        if cls.publisher is None:
            cls.publisher = publisher
