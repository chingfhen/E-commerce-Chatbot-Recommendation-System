import requests
from bot_world_classes import Product
import json
import sys
sys.path.append("..")
from bot_world_config import load_telegram_bot_config, load_seller_config


def send_recommendation(chat_id, product: Product, config):

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
    CONFIG = load_telegram_bot_config()
    CONFIG.update(load_seller_config())
    send_recommendation(chat_id = 513516525, 
                        product = Product(product_id = 23826146098, product_name = "a product name", categories = "a product category", image_url = "https://cf.shopee.sg/file/sg-11134207-23020-9nqha14zvsnvf4"),
                        config = CONFIG)
    print("Telegram Messages Send Success!")  

