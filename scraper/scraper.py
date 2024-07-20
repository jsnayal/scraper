import os

import requests
from bs4 import BeautifulSoup
from scraper.models import Settings
from scraper.database import Database, JSONDatabase
from scraper.cache import Cache


class Scraper:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.db: Database = JSONDatabase()
        self.cache = Cache()
        self.base_url = "https://dentalstall.com/shop/"

    def fetch_page(self, page_number):
        try:
            response = requests.get(f"{self.base_url}?page={page_number}", proxies=self.settings.proxy)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page {page_number}: {e}")
            return None

    def parse_page(self, html):
        soup = BeautifulSoup(html, "html.parser")
        products = []
        for product in soup.select(".product-inner"):
            title = product.select_one('.woo-loop-product__title a').text.strip()
            price = product.select_one('.woocommerce-Price-amount').text.strip()
            image_url = product.select_one('.mf-product-thumbnail img')['src']
            products.append({"title": title, "price": price, "image_url": image_url})
        return products

    def download_image(self, url, path):
        response = requests.get(url)
        with open(path, "wb") as file:
            file.write(response.content)

    def run(self):
        scraped_count = 0
        for page in range(1, self.settings.page_limit + 1):
            html = self.fetch_page(page)
            if not html:
                continue
            products = self.parse_page(html)
            for product in products:
                if not self.cache.is_cached(product):
                    directory_path = 'images'
                    if not os.path.exists(directory_path):
                        os.mkdir(directory_path)
                    image_path = f"{directory_path}/{product['title'].replace(' ', '_')}.jpg"
                    self.download_image(product["image_url"], image_path)
                    product["image_path"] = image_path
                    self.db.save_product(product)
                    self.cache.cache_product(product)
                    scraped_count += 1
        print(f"Scraped {scraped_count} products")
        return {"count": scraped_count}
