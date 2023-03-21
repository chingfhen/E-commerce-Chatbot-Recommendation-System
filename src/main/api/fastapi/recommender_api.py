import pandas as pd
import json
from fastapi import FastAPI

from db import establish_database_connection, get_products
from model import load_sar_model
from bot_world_classes import Query, Product, SessionRecommendations
from telegram_bot_messages import send_recommendation
from session import load_session

import sys
sys.path.append("..")
from bot_world_config import *


# load config
CONFIG = {}
CONFIG.update(load_database_config())
CONFIG.update(load_model_config())
CONFIG.update(load_session_config())
CONFIG.update(load_seller_config())
CONFIG.update(load_sar_config())
CONFIG.update(load_telegram_bot_config())
print("Config Load Success!")


# Create session
global_session = load_session()
print("Session Load Success!")

# connect database
global_database_connection = establish_database_connection(CONFIG)
print("Database Connection Success!")

# load model
global_model = load_sar_model(CONFIG)
print("Model Load Success!")

"""
FASTAPI
"""
app = FastAPI()
@app.get("/")
async def recommend():
    return {"response": "Welcome to Bot.World!"}
"""
Standard Recommendation
Input: Query
Output: {"recommendations": [item123,item321]}
"""
# @app.post("/recommend")
@app.post("/recommend")
async def recommend(query: Query):
    model_output = global_model.recommend_k_items(pd.DataFrame({"user_id":[query.user_id]}), top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"], remove_seen=True)
    item_ids = model_output[config["COL_ITEM"]].tolist()
    return {"recommendations": item_ids}
"""
ManyChat Response
Input: Query
Output: 
    - 1 item recommendation
    - item details e.g. title, product url, image url
"""
@app.post("/manychat/recommend")
async def manychat_recommend(query: Query):

    if not global_session.exists(query.user_id):
        # call the model
        model_output = global_model.recommend_k_items(pd.DataFrame({"user_id":[query.user_id]}), top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"], remove_seen=True)
        item_ids = list(map(int, model_output[CONFIG["COL_ITEM"]].tolist()))
        # call the database
        products = get_products(global_database_connection, item_ids, CONFIG)    
        # add to session
        global_session.add(user_id = query.user_id, recommendations = products)
        print("Made model and database call. Created User Session")
    
    item = global_session.recommend(user_id = query.user_id)

    send_recommendation(query.chat_id, item, CONFIG)
    
    return {
        "version": "v2",
        "content": {
            "type":"telegram",
            "messages": [
                # {
                #     "type": "image",
                #     "url": image_url,
                #     "buttons": [
                #         {
                #             "type": "url",
                #             "caption": "Product Link",
                #             "url": product_url,
                #             "webview_size": "full"
                #         },
                #         {
                #             "type": "url",
                #             "caption": config['SHOP_NAME'],
                #             "url": config['SHOP_URL'],
                #             "webview_size": "full"
                #         }
                #     ]
                # },
                # {
                #     "type": "text",
                #     "text": product_name
                # }
                ],
            # "actions": [],
            # "quick_replies": []
        }
    }

