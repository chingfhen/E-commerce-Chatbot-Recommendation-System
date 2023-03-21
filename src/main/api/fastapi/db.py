import sys
sys.path.append("..")
from bot_world_config import load_database_config
from bot_world_classes import Product
import mysql.connector
import os
import sqlite3


def establish_database_connection(config):
    if os.environ.get("USE_RDS"):
        database_connection = mysql.connector.connect(
            user=config['DATABASE_USER'], password=config['DATABASE_PASSWORD'],
            host=config['DATABASE_HOST'],
            database=config['DATABASE_NAME'], port = 3306
        )
    else:
        IN_DOCKER = not os.environ.get("USERNAME","unknown") =="tanch"
        if IN_DOCKER:
            database_connection = sqlite3.connect(config['DATABASE_PATH_DOCKER'])
        else:
            database_connection = sqlite3.connect(config['DATABASE_PATH_TANCH'])
    return database_connection

"""
Get info of 1 item 
"""
def get_product(database_connection, item_id, config):
    cur = database_connection.cursor()
    cur.execute(f"select * from {config['PRODUCT_INFO_TABLE_NAME']} where product_id={item_id};")
    item = next(cur)
    return Product(product_id = item[0], product_name = item[1], categories = item[2], image_url = item[3])

"""
Get list of Product
"""
def get_products(database_connection, item_ids: list, config):
    cur = database_connection.cursor()
    comma_separated_item_ids = ",".join(map(str,item_ids))
    cur.execute(f"select * from {config['PRODUCT_INFO_TABLE_NAME']} where product_id in ({comma_separated_item_ids});")
    products = []
    for item in cur:
        products.append(Product(product_id = item[0], product_name = item[1], categories = item[2], image_url = item[3]))
    return products

if __name__ == "__main__":
    CONFIG = load_database_config()
    print("Config Load Success!")
    database_connection = establish_database_connection(CONFIG)
    print("Database Connection Success!")
    product = get_product(database_connection, 23821143235, CONFIG)
    products = get_products(database_connection, [23821143235], CONFIG)
    print("Product Retrieval Success!")
    print(product, products)