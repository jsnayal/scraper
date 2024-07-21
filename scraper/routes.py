from starlette.responses import JSONResponse

from scraper.models import Settings, Recipient
from fastapi import APIRouter, BackgroundTasks, status

from scraper.notification import MessagePublisher, Subscriber
from scraper.scraper import WebScraper

router = APIRouter()


@router.post("/scrape")
async def scrape(settings: Settings, background_tasks: BackgroundTasks):
    scraper = await WebScraper.get_scraper()
    background_tasks.add_task(scraper.run, settings)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Started scraping {settings.page_limit} pages. "
                       f"We will notify the recipients when the task is complete"
        }
    )


@router.post("/register_recipient")
async def register_recipient(recipient: Recipient):
    MessagePublisher.publisher.subscribers.append(
        Subscriber(name=recipient.name, email=recipient.email, phone=recipient.phone)
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"{recipient.name} is subscribed"},
    )
