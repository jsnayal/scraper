from fastapi import FastAPI
from scraper.scraper import Scraper
from scraper.models import Settings

app = FastAPI()


@app.post("/scrape")
async def scrape(settings: Settings):
    scraper = Scraper(settings)
    result = scraper.run()
    return {"message": f"Scraped {result['count']} products"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
