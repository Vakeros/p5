import mysql.connector

from constant import CATEGORIES
from constant import PRODUCTS
import requests

mydb = mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    auth_plugin='mysql_native_password'
)


class products:

    def __init__(self):
        self.data_products = []

    def get_api_data(self):
        for categories_key, categories_values in CATEGORIES.items():
            if categories_key:
                data = requests.get(categories_values + "1.json")
                data_json = data.json()
                products_data_json = data_json["products"]

                for prod in products_data_json:
                    try:
                        name = prod["generic_name_fr"]
                    except KeyError:
                        """" try:
                            name = prod["generic_name"]
                        except KeyError:
                            print("dead") """
                        name = ""
                    try:
                        score = prod["nutriscore_score"]
                    except KeyError:
                        score = "X"
                    try:
                        url = prod["url"]
                    except KeyError:
                        url = "unknown"
                    try:
                        store = prod["stores"]
                    except KeyError:
                        store = "unknown"
                    self.data_products.append([name, url, categories_key, store, score])

    def insert_data(self):
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS p5")
        mydb.database = "p5"
        mycursor.execute("CREATE TABLE IF NOT EXISTS `p5`.`product` ( `id` INT NOT NULL AUTO_INCREMENT ,"
                         " `name` VARCHAR(255) NOT NULL,"
                         " `url` VARCHAR(1000) NOT NULL UNIQUE,"
                         " `categorie` VARCHAR(255) NOT NULL,"
                         " `store` VARCHAR(255) NOT NULL,"
                         " `score` VARCHAR(255) , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
        sql = "INSERT IGNORE INTO product (name, url, categorie, store ,score) VALUES (%s, %s, %s, %s, %s)"
        val = []
        for product in self.data_products:
            val.append(product)

        mycursor.executemany(sql, val)
        mydb.commit()

    def get_products(self, categorie):
        mycursor = mydb.cursor()
        sql = "SELECT * FROM product WHERE categorie = %s"
        categorie = (categorie,)
        mycursor.execute(sql, categorie)
        data = mycursor.fetchall()
        return data

    def client_save_product(self, id):
        mycursor = mydb.cursor()
        sql = "INSERT INTO user (product) VALUES (%s)"
        id = (id,)
        mycursor.execute(sql, id)
        mydb.commit()

    def client_get_product(self):
        mycursor = mydb.cursor()
        sql = "SELECT name,url,store,score FROM product,user WHERE product.id =  user.product"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        return data
