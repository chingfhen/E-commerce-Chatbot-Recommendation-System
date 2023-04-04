import requests
from bot_world_classes import TelegramRecommendation, Product
import json
import sys
sys.path.append("..")
from bot_world_config import load_telegram_bot_config, load_seller_config

"""
Sends Image request to Telegram Bot API
"""
def send_telegram_image(config, telegram_recommendation: TelegramRecommendation):

    r = requests.post(
            url = f"https://api.telegram.org/bot{config['BOT_TOKEN']}/sendPhoto", 
            data = {
                "chat_id": telegram_recommendation.chat_id, 
                "photo": telegram_recommendation.item.image_url
            }
        )

"""
Sends recommendation via Telegram Bot API
"""
def send_telegram_recommendation(config, telegram_recommendation: TelegramRecommendation):

    r = requests.post(
            url = f"https://api.telegram.org/bot{config['BOT_TOKEN']}/sendPhoto", 
            data = {
                "chat_id": telegram_recommendation.chat_id, 
                "photo": telegram_recommendation.item.image_url,
                "caption": telegram_recommendation.item.product_name,
                "reply_markup":json.dumps({
                "inline_keyboard":[[
                        {
                        "text":"Purchase Item",
                        "url":f"https://shopee.sg/product/{config['SELLER_ID']}/{telegram_recommendation.item.product_id}"
                        }
                    ]]
                })
            }
        )


if __name__=="__main__":
    CONFIG = load_telegram_bot_config()
    CONFIG.update(load_seller_config())
    send_telegram_image(
        config = CONFIG, 
        telegram_recommendation = TelegramRecommendation(
            chat_id = 513516525, 
            item = Product(product_id = 23826146098, product_name = "a product name", categories = "a product category", image_url = "https://cf.shopee.sg/file/sg-11134207-23020-9nqha14zvsnvf4")
        )                    
    )
    print("Telegram Messages Send Success!")  
    # send_telegram_recommendation(
    #     config = CONFIG, 
    #     telegram_recommendation = TelegramRecommendation(
    #         chat_id = 513516525, 
    #         item = Product(product_id = 23826146098, product_name = "a product name", categories = "a product category", image_url = "https://cf.shopee.sg/file/sg-11134207-23020-9nqha14zvsnvf4")
    #     )                    
    # )
    # print("Telegram Messages Send Success!")  