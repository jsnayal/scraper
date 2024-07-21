from scraper.models import Settings, Recipient
from fastapi import APIRouter

from scraper.scraper import WebScraper

router = APIRouter()


@router.post("/scrape")
async def scrape(settings: Settings):
    scraper = WebScraper.get_scraper()
    result = await scraper.run(settings)
    return result


@router.post("/scrape")
async def register_recipient(recipient: Recipient):
    result = await scraper.run(settings)
    return result
