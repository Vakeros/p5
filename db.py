"""db"""
import mysql.connector
from api import API

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
        print("Creation de la base de donnée ...")
        mycursor = MYDB.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS p5")
        MYDB.database = "p5"
        mycursor.execute("CREATE TABLE IF NOT EXISTS `p5`.`product`"
                         " ( `id` INT NOT NULL AUTO_INCREMENT ,"
                         " `name` VARCHAR(255) NOT NULL,"
                         " `url` VARCHAR(1000) NOT NULL UNIQUE,"
                         " `categorie` INT NOT NULL,"
                         " `store` VARCHAR(255) NOT NULL,"
                         " `score` VARCHAR(255), PRIMARY KEY (`id`))"
                         "  ENGINE = InnoDB;")
        mycursor.execute("CREATE TABLE IF NOT EXISTS `p5`.`user`"
                         " ( `id` INT NOT NULL AUTO_INCREMENT ,"
                         " `product` INT(11) , PRIMARY KEY (`id`)) ENGINE = InnoDB;"
                        )
        mycursor.execute("CREATE TABLE IF NOT EXISTS `p5`.`category`"
                         " ( `id` INT NOT NULL AUTO_INCREMENT ,"
                         " `categorie` VARCHAR(255)  ,"
                         " PRIMARY KEY (`id`)) ENGINE = InnoDB;"
                         )
        mycursor.execute("""ALTER TABLE product ADD CONSTRAINT FK_CAT
                          FOREIGN KEY IF NOT EXISTS (categorie)
                          REFERENCES Category (id)
                          ON DELETE NO ACTION
                          ON UPDATE NO ACTION;
                          """)
        mycursor.execute("""ALTER TABLE user ADD CONSTRAINT FK_U
                            FOREIGN KEY IF NOT EXISTS (product)
                            REFERENCES product (id)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION;
                            """)
        print("Done")

    def get_api_data(self):
        """get data from openfoodfact API"""
        self.data_products = API.products

    def insert_data(self):
        """create and insert data into database"""
        mycursor = MYDB.cursor()
        sql = "INSERT IGNORE INTO product (name, url, categorie, store ,score)" \
              " VALUES (%s, %s, %s, %s, %s)"
        cat_sql = "INSERT IGNORE INTO category (id, categorie)" \
                  " VALUES (%s, %s)"
        val = []
        cat_val = []

        for cat in API.categories:
            cat_val.append(["", cat["name"]])

        for product in self.data_products:
            val.append(product.get_all())

        mycursor.executemany(cat_sql, cat_val)
        mycursor.executemany(sql, val)

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
        categorie = (categorie+1,)
        mycursor.execute(sql, categorie)
        data = mycursor.fetchall()
        return data

    @staticmethod
    def client_save_product(pid):
        """save client substitue products"""
        mycursor = MYDB.cursor()
        sql = "INSERT INTO user (product) VALUES (%s)"
        mycursor.execute(sql, (pid,))
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
