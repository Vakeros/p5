import mysql.connector
from constant import CATEGORIES
from constant import PRODUCTS
from constant import CAT
import os
import requests
import json
from products import products

db = products()
db.get_api_data()
db.insert_data()
len_categorie = len(CATEGORIES)
categorie_name = []


def remplace():
    try:
        while True:
            products_list = []
            value = 0
            for i in CATEGORIES:
                print(str(value) + ": " + i)
                categorie_name.append(i)
                value += 1
            choice = int(input("Indiquez le numéro d'une categorie :"))
            data = db.get_products(CAT[categorie_name[choice]])
            for i in data:
                if i[PRODUCTS["name"]] != "" and i[PRODUCTS["name"]] != "unknown":
                    products_list.append(i)
            for index, data in enumerate(products_list):
                print(str(index) + " " + data[PRODUCTS["name"]])
            choice = int(input("Indiquez l'id'd'un produit :"))
            for data in products_list:
                if data[PRODUCTS["score"]] > products_list[choice][PRODUCTS["score"]]:
                    print("nous vous proposons " + data[PRODUCTS["name"]] + " achetable a " + data[PRODUCTS["store"]])
                    if input("souhaitez vous enregistrez cette proposition ? y/n :") == "y":
                        db.client_save_product(data[PRODUCTS["id"]])
                        print("sauvegarde")
                    return
    except ValueError:
        print("entrer une valeur entre 0 et " + str(len_categorie - 1))

def get_client_data():
    data = db.client_get_product()
    for i in data:
        print("name: " +i[0] + " store: " +i[2] + " score: " + str(i[3]))

while True:
    try:
        print("1: Quel aliment souhaitez-vous remplacer ?")
        print("2: Retrouver mes aliments substitués.")
        choice = int(input())
        if choice == 1:
            remplace()
        elif choice == 2:
            get_client_data()
        else:
            print("entrer une valeur entre 1 et 2")
    except ValueError:
        print("entrer une valeur entre 1 et 2")