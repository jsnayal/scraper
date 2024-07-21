import os
import requests
from bs4 import BeautifulSoup

from scraper.constants import RETRY_SECONDS, RETRY_COUNT
from scraper.models import Settings
from scraper.database import Database
from scraper.cache import Cache
from scraper.notification import MessagePublisher
from typing import Dict, Tuple
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type


class Scraper:
    def __init__(self, database: Database, cache: Cache):
        self.db = database
        self.cache = cache
        self.base_url = "https://dentalstall.com/shop"

    @retry(wait=wait_fixed(RETRY_SECONDS), stop=stop_after_attempt(RETRY_COUNT), retry=retry_if_exception_type(requests.RequestException))
    def fetch_page(self, page_number: int, proxy: Dict[str, str]) -> str:
        try:
            response = requests.get(f"{self.base_url}/page/{page_number}", proxies=proxy)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page {page_number}: {e}")
            raise

    def parse_page(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        products = []
        for product in soup.select(".product-inner"):
            title = product.select_one('.woo-loop-product__title a').text.strip()
            price = product.select_one('.woocommerce-Price-amount').text.strip()
            image_url = product.select_one('.mf-product-thumbnail img')['data-lazy-src']
            products.append({"product_title": title, "product_price": float(price[1:]), "image_url": image_url})
        return products

    def download_image(self, url: str, path: str) -> None:
        response = requests.get(url)
        with open(path, "wb") as file:
            file.write(response.content)

    async def run(self, settings: Settings) -> dict:
        total_scraped_count = 0
        for page in range(1, settings.page_limit + 1):
            is_scraped, scraped_count = await self.scrape_page(page, settings)
            if not is_scraped:
                # Retry logic is handled within fetch_page
                pass
            else:
                total_scraped_count += scraped_count
        message = {"message": f"Scraped {total_scraped_count} products"}
        MessagePublisher.publisher.publish(message)
        return message

    async def scrape_page(self, page: int, settings: Settings) -> Tuple[bool, int]:
        scraped_count = 0
        try:
            html = self.fetch_page(page, settings.proxy)
            if not html:
                raise Exception("Invalid html")
            products = self.parse_page(html)
            for product in products:
                if not self.cache.is_cached(product):
                    directory_path = 'images'
                    if not os.path.exists(directory_path):
                        os.mkdir(directory_path)
                    image_path = f"{directory_path}/{product['product_title'].replace(' ', '_')}.jpg"
                    self.download_image(product["image_url"], image_path)
                    product["path_to_image"] = image_path
                    self.db.save_product(product)
                    self.cache.cache_product(product)
                    scraped_count += 1
            is_scraped = True
        except Exception as ex:
            print(f"Error scraping page {page}: {ex}")
            is_scraped = False
        return is_scraped, scraped_count


class WebScraper:
    scraper: Scraper = None

    @classmethod
    async def get_scraper(cls):
        return cls.scraper

    @classmethod
    def set_scraper(cls, scraper):
        if cls.scraper is None:
            cls.scraper = scraper
