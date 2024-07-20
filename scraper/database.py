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
        self.file_path = "products.json"

    def save_product(self, product):
        try:
            if not os.path.exists(self.file_path):
                os.mknod(self.file_path)
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        data.append(product)
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def get_all_products(self):
        NotImplementedError()
