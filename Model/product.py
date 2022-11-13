import json
from json import JSONEncoder


class Product:
    name = None
    barcode = None
    image_url = None
    category = None

    def __init__(self, name, barcode, image_url, category):
        self.name = name
        self.barcode = barcode
        self.image_url = image_url
        self.category = category


class ProductEncoder(JSONEncoder):

    def default(self, product):

        if isinstance(product, Product):
            return product.__dict__
        else:
            return json.JSONEncoder.default(self, product)