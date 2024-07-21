from fastapi import FastAPI
import uvicorn
from scraper.cache import RedisCache
from scraper.constants import DatabaseType, CacheType, NotificationType
from scraper.database import JSONDatabase
from scraper.middleware import TokenAuthMiddleware
from scraper.notification import ConsoleNotification, MessagePublisher, Publisher
from scraper.routes import router
from scraper.scraper import Scraper, WebScraper

app = FastAPI()
app.include_router(router)
app.add_middleware(TokenAuthMiddleware)


def initialize_scraper(database: DatabaseType, cache: CacheType, notification: NotificationType) -> Scraper:
    """
    Initializes and returns a Scraper instance with specified database, cache, and notification strategies
    :param database: The type of database to use
    :param cache: The type of cache to use
    :param notification: The type of notification strategy to use
    :return: An instance of the Scraper class initialized with the specified strategies
    """
    db_instance = {
        DatabaseType.JSON: JSONDatabase(),
        # add other database strategy here
    }.get(database)

    cache_instance = {
        CacheType.REDIS: RedisCache(),
        # add other cache strategy here
    }.get(cache)

    notifier_instance = {
        NotificationType.CONSOLE: ConsoleNotification(),
        # add other notification strategy here
    }.get(notification)

    # publisher instance with chosen notification strategy
    publisher = Publisher(notification=notifier_instance)
    MessagePublisher.set_publisher(publisher)
    return Scraper(database=db_instance, cache=cache_instance)


if __name__ == "__main__":
    WebScraper.set_scraper(initialize_scraper(DatabaseType.JSON, CacheType.REDIS, NotificationType.CONSOLE))
    uvicorn.run(app, host="127.0.0.1", port=8000)
