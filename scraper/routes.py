from scraper.models import Settings, Recipient
from fastapi import APIRouter

from scraper.notification import MessagePublisher, Subscriber
from scraper.scraper import WebScraper

router = APIRouter()


@router.post("/scrape")
async def scrape(settings: Settings):
    scraper = WebScraper.get_scraper()
    result = await scraper.run(settings)
    return result


@router.post("/register_recipient")
async def register_recipient(recipient: Recipient):
    MessagePublisher.publisher.subscribers.append(
        Subscriber(name=recipient.name, email=recipient.email, phone=recipient.phone)
    )
    return {"message": f"{recipient.name} is subscribed"}
