from fastapi import FastAPI

from scraper.cache import RedisCache
from scraper.constants import DatabaseType, CacheType, NotificationType
from scraper.database import JSONDatabase
from scraper.middleware import TokenAuthMiddleware
from scraper.notification import ConsoleNotification
from scraper.scraper import Scraper
from scraper.models import Settings

app = FastAPI()
app.add_middleware(TokenAuthMiddleware)
scraper: Scraper


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


@app.post("/scrape")
async def scrape(settings: Settings):
    result = await scraper.run(settings)
    return result

if __name__ == "__main__":
    import uvicorn
    scraper = initialize_scraper(DatabaseType.JSON, CacheType.REDIS, NotificationType.CONSOLE)
    uvicorn.run(app, host="127.0.0.1", port=8000)
