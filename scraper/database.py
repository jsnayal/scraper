import json
import os
from abc import ABC, abstractmethod


class Database(ABC):
    """
    Abstract base class for a database.
    This class defines the interface that any concrete database implementation must adhere to
    """

    @abstractmethod
    def save_product(self, product):
        """
        Save a product to the database
        :param product: product to be saved
        :return: None
        """
        NotImplementedError()

    @abstractmethod
    def get_all_products(self):
        """
        Retrieve all products from the database
        Raises: NotImplementedError: If the method is not implemented by a subclass
        """
        NotImplementedError()


class JSONDatabase(Database):
    """
    Concrete implementation of the Database interface using JSON files
    This class handles saving products to and retrieving products from a JSON file
    """
    def __init__(self):
        self.output_dir = os.path.join(os.getcwd(), 'output')
        self.file_path = os.path.join(self.output_dir, "products.json")

    def save_product(self, product) -> None:
        """
        Save a product to the JSON file
        :param product: product to be saved
        :return: None
        """
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
        """
        Retrieve all products from the JSON file.
        :return: Not Implemented
        """
        NotImplementedError()
