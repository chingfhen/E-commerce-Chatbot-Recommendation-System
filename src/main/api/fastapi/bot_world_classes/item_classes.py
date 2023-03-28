from pydantic import BaseModel
from typing import Optional

"""
A Product Recommendation
"""
class Product(BaseModel):
    product_id: int
    product_name: str
    categories: str
    image_url: str

"""
Query format for sending a recommendation
"""
class TelegramRecommendation(BaseModel):
    chat_id: int
    item: Product


if __name__ == "__main__":
    product = Product(product_id = 23826146098, 
                    product_name = "a product name", 
                    categories = "a product category", 
                    image_url = "https://cf.shopee.sg/file/sg-11134207-23020-9nqha14zvsnvf4")
    print("Created Product: ")
    print(product)

    telegram_recommendation = TelegramRecommendation(chat_id = 123, 
                                    item = product)
    print("Created TelegramRecommendQuery: ")
    print(telegram_recommendation)