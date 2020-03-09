"""API openfoodfact"""
import requests
from constant import CATEGORIES_COUNT, PAGE_COUNT
from products import Product


class API:
    """API"""
    categories = []
    products = []

    @staticmethod
    def load():
        """loading data"""
        API.clear()
        API.__get_cat()
        API.__get_products()

    @staticmethod
    def clear():
        """clear all data"""
        API.categories.clear()
        API.products.clear()

    @staticmethod
    def __get_cat():
        print("Récupération des catégories... ")
        data = requests.get("https://fr.openfoodfacts.org/categories.json")
        data = data.json()
        value = CATEGORIES_COUNT
        for cat in data["tags"]:
            API.categories.append(cat)
            value -= 1
            if value <= 0:
                print("Done")
                return
        print("Done")


    @staticmethod
    def __get_products():
        """get data from openfoodfact API"""
        i = 0
        for categories_values in API.categories:
            print("Récupération des produits " + str(i+1) + " / " + str(len(API.categories)))
            for page in range(1, PAGE_COUNT + 1):
                data = requests.get(categories_values["url"] + "/" + str(page) + ".json")
                data_json = data.json()
                products_data_json = data_json["products"]

                for prod in products_data_json:

                    product = Product([
                        prod.get("product_name_fr", ""),
                        prod.get("url"),
                        prod.get("stores", ""),
                        prod.get("nutriscore_grade", "X"),
                        i + 1
                    ])

                    if prod.get("product_name_fr", "") != "" \
                            and prod.get("generic_name_fr", "") != "unknown" \
                            and prod.get("nutriscore_grade", "X") != "X" \
                            and prod.get("stores", "") != "":
                        API.products.append(product)
            i += 1
        print("Done")
