import json
import os
from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def save_product(self, product):
        NotImplementedError()

    @abstractmethod
    def get_all_products(self):
        NotImplementedError()


class JSONDatabase(Database):
    def __init__(self):
        self.output_dir = os.path.join(os.getcwd(), 'output')
        self.file_path = os.path.join(self.output_dir, "products.json")

    def save_product(self, product) -> None:
        try:
            if not os.path.exists(self.output_dir):
                os.mkdir(self.output_dir)
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except Exception:
            data = []
        data.append(product)
        with open(self.file_path, "w+") as file:
            json.dump(data, file, indent=4)

    def get_all_products(self):
        NotImplementedError()
