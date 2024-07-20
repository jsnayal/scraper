from fastapi import FastAPI

from scraper.cache import RedisCache
from scraper.constants import DatabaseType, CacheType, NotificationType
from scraper.database import JSONDatabase
from scraper.middleware import TokenAuthMiddleware
from scraper.notification import ConsoleNotification
from scraper.routes import router
from scraper.scraper import Scraper, WebScraper

app = FastAPI()
app.include_router(router)
app.add_middleware(TokenAuthMiddleware)


def initialize_scraper(database: DatabaseType, cache: CacheType, notification: NotificationType) -> Scraper:
    db_instance = {
        DatabaseType.JSON: JSONDatabase(),
        # add other databases
    }.get(database)

    cache_instance = {
        CacheType.REDIS: RedisCache(),
        # add other databases
    }.get(cache)

    notifier_instance = {
        NotificationType.CONSOLE: ConsoleNotification(),
        # add other databases
    }.get(notification)

    return Scraper(database=db_instance, cache=cache_instance, notification=notifier_instance)


if __name__ == "__main__":
    import uvicorn
    WebScraper.set_scraper(initialize_scraper(DatabaseType.JSON, CacheType.REDIS, NotificationType.CONSOLE))
    uvicorn.run(app, host="127.0.0.1", port=8000)
