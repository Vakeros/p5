"""products"""


class Product:
    """Product class"""

    def __init__(self, data):
        """init product"""
        self.name = data[0]
        self.url = data[1]
        self.store = data[2]
        self.score = data[3]
        self.category = data[4]

    def get_all(self):
        """get all data"""
        return [self.name, self.url, self.category, self.store, self.score]

    def product_print(self):
        """print product"""
        print("name : " + self.name + "url :" + self.url + "store : " + self.store)
