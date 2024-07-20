from fastapi import FastAPI

from scraper.cache import RedisCache
from scraper.constants import DatabaseType, CacheType
from scraper.database import JSONDatabase
from scraper.scraper import Scraper
from scraper.models import Settings

app = FastAPI()

scraper: Scraper


def initialize_scraper(database: DatabaseType, cache: CacheType) -> Scraper:
    db_instance = {
        DatabaseType.JSON: JSONDatabase(),
        # add other databases
    }.get(database)

    cache_instance = {
        CacheType.REDIS: RedisCache(),
        # add other databases
    }.get(cache)

    return Scraper(database=db_instance, cache=cache_instance)


@app.post("/scrape")
async def scrape(settings: Settings):
    result = scraper.run(settings)
    return {"message": f"Scraped {result['count']} products"}

if __name__ == "__main__":
    import uvicorn
    scraper = initialize_scraper(DatabaseType.JSON, CacheType.REDIS)
    uvicorn.run(app, host="127.0.0.1", port=8000)
