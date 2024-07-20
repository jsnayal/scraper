from scraper.models import Settings
from fastapi import APIRouter

from scraper.scraper import WebScraper

router = APIRouter()


@router.post("/scrape")
async def scrape(settings: Settings):
    scraper = WebScraper.get_scraper()
    result = await scraper.run(settings)
    return result
