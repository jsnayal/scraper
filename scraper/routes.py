from starlette.responses import JSONResponse

from scraper.models import Settings, Recipient
from fastapi import APIRouter, BackgroundTasks, status

from scraper.notification import MessagePublisher, Subscriber
from scraper.scraper import WebScraper

router = APIRouter()


@router.post("/scrape")
async def scrape(settings: Settings, background_tasks: BackgroundTasks):
    """
    Initiates a web scraping task in the background
    :param settings: settings provided in the input. e.g. page count to scrape and proxy string
    :param background_tasks: this is to add the scraping task as async background task
    :return: JSON response indicating the scraping task has started
    """
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
    """
    :param recipient: recipient to be register and notified
    :return: JSON response indicating the recipient has been subscribed
    """
    MessagePublisher.publisher.subscribers.append(
        Subscriber(name=recipient.name, email=recipient.email, phone=recipient.phone)
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"{recipient.name} is subscribed"},
    )
