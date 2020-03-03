"""substitue"""
from constant import CATEGORIES, PRODUCTS, SCORE
from db import DB


class Substitute:
    """Substitue"""
    def __init__(self):
        self.db = DB()
        self.len_categorie = len(CATEGORIES)
        self.categories_name = []
        self.category = self.db.get_cat()

    def remplace(self):
        """remplace selected product"""
        try:
            while True:

                products_list = []
                value = 0
                for i in CATEGORIES:
                    print(str(value) + ": " + i)
                    self.categories_name.append(i)
                    value += 1

                entry = int(input("entrer le numéro d'une categorie :"))
                try:
                    data = self.db.get_products(self.category[self.categories_name[entry]])
                except IndexError:
                    self.remplace()
                for i in data:
                    products_list.append(i)

                for index, data in enumerate(products_list):
                    print(str(index) + " " + data[PRODUCTS["name"]])

                entry = int(input("Indiquez l'id'd'un produit :"))
                for data in products_list:
                    if SCORE[data[PRODUCTS["score"]]] < SCORE[products_list[entry][PRODUCTS["score"]]]:
                        print(
                            "nous vous proposons " +
                            data[PRODUCTS["name"]] +
                            " achetable a " +
                            data[PRODUCTS["store"]]
                        )
                        if input("souhaitez vous enregistrez cette proposition ? y/n :") == "y":
                            self.db.client_save_product(data[PRODUCTS["id"]])
                            print("sauvegarde")
                        return
                print("aucun produit de substitution n'a été trouvé")
        except ValueError:
            print("entrer une valeur entre 0 et " + str(self.len_categorie - 1))

    def get_client_data(self):
        """get client substitute products"""
        data = self.db.client_get_product()
        for i in data:
            print("name: " + i[0] + " store: " + i[2] + " score: " + str(i[3]))
