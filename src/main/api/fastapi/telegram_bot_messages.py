import requests
from classes import Product
import json
import os
import yaml


# load config
config = {}
local_path = r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\config\telegram-bot-config.yaml"
volume_path = "/config/telegram-bot-config.yaml"
config_path = local_path if os.path.exists(local_path) else volume_path
with open(config_path, "r") as f:
    try:
        config.update(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)

local_path = r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\config\seller-config.yaml"
volume_path = "/config/seller-config.yaml"
config_path = local_path if os.path.exists(local_path) else volume_path
with open(config_path, "r") as f:
    try:
        config.update(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)


def send_recommendation(chat_id, product: Product):

    r = requests.post(
            url = f"https://api.telegram.org/bot{config['BOT_TOKEN']}/sendPhoto", 
            data = {
                "chat_id": chat_id, 
                "photo": product.image_url,
                "caption": product.product_name,
                "reply_markup":json.dumps({
                "inline_keyboard":[[
                        {
                        "text":"More Info",
                        "url":f"https://shopee.sg/product/{config['SELLER_ID']}/{product.product_id}"
                        }
                    ]]
                })
            }
        )


if __name__=="__main__":
    print("Done")  

