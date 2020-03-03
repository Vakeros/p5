"""db"""
import mysql.connector
import requests
from constant import CATEGORIES, PAGE_COUNT
from products import Product

MYDB = mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    auth_plugin='mysql_native_password'
)


class DB:
    """Data base"""
    def __init__(self):
        self.data_products = []
        self.create_data_base()
        self.get_api_data()
        self.insert_data()

    @staticmethod
    def create_data_base():
        """create data base and table"""
        mycursor = MYDB.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS p5")
        MYDB.database = "p5"
        mycursor.execute("CREATE TABLE IF NOT EXISTS `p5`.`product`"
                         " ( `id` INT NOT NULL AUTO_INCREMENT ,"
                         " `name` VARCHAR(255) NOT NULL,"
                         " `url` VARCHAR(1000) NOT NULL UNIQUE,"
                         " `categorie` VARCHAR(255) NOT NULL,"
                         " `store` VARCHAR(255) NOT NULL,"
                         " `score` VARCHAR(255), PRIMARY KEY (`id`),"
                         " INDEX cat (categorie)) ENGINE = InnoDB;")
        mycursor.execute("CREATE TABLE IF NOT EXISTS `p5`.`user`"
                         " ( `id` INT NOT NULL AUTO_INCREMENT ,"
                         " `product` INT(11) , PRIMARY KEY (`id`)) ENGINE = InnoDB;"
                        )
        mycursor.execute("CREATE TABLE IF NOT EXISTS `p5`.`category`"
                         " ( `id` INT NOT NULL AUTO_INCREMENT ,"
                         " `categorie` VARCHAR(255) UNIQUE ,"
                         " PRIMARY KEY (`id`)) ENGINE = InnoDB;"
                         )

    def get_api_data(self):
        """get data from openfoodfact API"""
        i = 0
        print("Loading ...")
        for categories_key, categories_values in CATEGORIES.items():
            if categories_key:
                for y in range(1, PAGE_COUNT+1):
                    data = requests.get(categories_values + str(y) + ".json")
                    data_json = data.json()
                    products_data_json = data_json["products"]

                    for prod in products_data_json:
                        product = Product([
                            prod.get("generic_name_fr", ""),
                            prod.get("url"),
                            prod.get("stores", ""),
                            prod.get("nutriscore_grade", "X"),
                            i+1
                        ])

                        if prod.get("generic_name_fr", "") != ""\
                                and prod.get("generic_name_fr", "") != "unknown"\
                                and prod.get("nutriscore_grade", "X") != "X"\
                                and prod.get("stores", "") != "":
                            self.data_products.append(product)
            i += 1

    def insert_data(self):
        """create and insert data into database"""
        mycursor = MYDB.cursor()
        sql = "INSERT IGNORE INTO product (name, url, categorie, store ,score)" \
              " VALUES (%s, %s, %s, %s, %s)"
        cat_sql = "INSERT IGNORE INTO category (id, categorie)" \
                  " VALUES (%s, %s)"
        val = []
        cat_val = []

        for cat in CATEGORIES:
            cat_val.append(["", cat])

        for product in self.data_products:
            val.append(product.get_all())

        mycursor.executemany(sql, val)
        mycursor.executemany(cat_sql, cat_val)
        MYDB.commit()

    @staticmethod
    def get_cat():
        """get category from database"""
        mycursor = MYDB.cursor()
        sql = "SELECT * FROM category"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        cat_list = {}
        for element in data:
            cat_list[element[1]] = element[0]
        return cat_list

    @staticmethod
    def get_products(categorie):
        """get products from database"""
        print(categorie)
        mycursor = MYDB.cursor()
        sql = "SELECT * FROM product WHERE categorie = %s"
        categorie = (categorie,)
        mycursor.execute(sql, categorie)
        data = mycursor.fetchall()
        return data

    @staticmethod
    def client_save_product(id):
        """save client substitue products"""
        mycursor = MYDB.cursor()
        sql = "INSERT INTO user (product) VALUES (%s)"
        mycursor.execute(sql, (id,))
        MYDB.commit()

    @staticmethod
    def client_get_product():
        """get client substitue products"""
        mycursor = MYDB.cursor()
        sql = "SELECT name,url,store,score FROM product " \
              "INNER JOIN user ON product.id =  user.product"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        return data
