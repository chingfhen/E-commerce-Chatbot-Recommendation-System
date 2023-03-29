import pandas as pd
import json
from fastapi import FastAPI
from typing import Optional
from math import ceil

from db import establish_database_connection, get_products
from model import load_sar_model
from bot_world_classes import *
from telegram_bot_messages import send_telegram_recommendation
from session import load_session, get_session_id

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
async def root():
    return {"response": "Welcome to Bot.World!"}

"""
Documentation
"""
@app.post("/recommend")
async def recommend(recommend_request: RecommendRequest):
    
    recommended_item_ids = []
    
    if recommend_request.by == "user":
        model_output = global_model.recommend_k_items(test = pd.DataFrame({CONFIG["COL_USER"]:[recommend_request.user_id]}), 
                                                      top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"], 
                                                      remove_seen=True)
        recommended_item_ids = model_output[CONFIG["COL_ITEM"]].tolist()
    elif recommend_request.by == "item":
        model_output = global_model.get_item_based_topk(items = pd.DataFrame({CONFIG["COL_ITEM"]:[recommend_request.item_id]}), 
                                                        top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"])
        recommended_item_ids = model_output[CONFIG["COL_ITEM"]].tolist()
    elif recommend_request.by == "popularity":
        model_output = global_model.get_popularity_based_topk(top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"])
        recommended_item_ids = model_output[CONFIG["COL_ITEM"]].tolist()

    elif recommend_request.by =="hybrid":

        model_output_popularity_based = global_model.get_popularity_based_topk(top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"])
        recommended_item_ids.extend(model_output_popularity_based[CONFIG["COL_ITEM"]].tolist()[:ceil(CONFIG["SESSION_RECOMMENDATION_SIZE"]/2)])

        model_output_user_based = global_model.recommend_k_items(test = pd.DataFrame({CONFIG["COL_USER"]:[recommend_request.user_id]}), 
                                                                top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"]//2, 
                                                                remove_seen=True)
        recommended_item_ids.extend(model_output_user_based[CONFIG["COL_ITEM"]].tolist())

        
    return {"recommendations": recommended_item_ids}

"""
Documentation
"""
@app.post("/manychat/recommend")
async def manychat_recommend(chat_id: int, recommend_request: RecommendRequest):
    
    ID = get_session_id(chat_id = chat_id, by = recommend_request.by, user_id = recommend_request.user_id, item_id = recommend_request.item_id)

    # if session doesn't exist, then make a model and database call
    if not global_session.exists(ID = ID):

        recommended_item_ids = []
    
        if recommend_request.by == "user":
            model_output = global_model.recommend_k_items(test = pd.DataFrame({CONFIG["COL_USER"]:[recommend_request.user_id]}), 
                                                        top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"], 
                                                        remove_seen=True)
            recommended_item_ids = model_output[CONFIG["COL_ITEM"]].tolist()

        elif recommend_request.by == "item":
            model_output = global_model.get_item_based_topk(items = pd.DataFrame({CONFIG["COL_ITEM"]:[recommend_request.item_id]}), 
                                                            top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"])
            recommended_item_ids = model_output[CONFIG["COL_ITEM"]].tolist()

        elif recommend_request.by == "popularity":
            model_output = global_model.get_popularity_based_topk(top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"])
            recommended_item_ids = model_output[CONFIG["COL_ITEM"]].tolist()

        elif recommend_request.by =="hybrid":
            model_output_popularity_based = global_model.get_popularity_based_topk(top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"])
            recommended_item_ids.extend(model_output_popularity_based[CONFIG["COL_ITEM"]].tolist()[:ceil(CONFIG["SESSION_RECOMMENDATION_SIZE"]/2)])

            model_output_user_based = global_model.recommend_k_items(test = pd.DataFrame({CONFIG["COL_USER"]:[recommend_request.user_id]}), 
                                                                    top_k=CONFIG["SESSION_RECOMMENDATION_SIZE"]//2, 
                                                                    remove_seen=True)
            recommended_item_ids.extend(model_output_user_based[CONFIG["COL_ITEM"]].tolist())

        # DATABASE CALL
        products = get_products(CONFIG, global_database_connection, recommended_item_ids)   

        # add to session
        global_session.add(ID = ID, recommendations = products) 

    # retrieve 1 recommendation from session
    item = global_session.recommend(ID = ID)

    telegram_recommendation = TelegramRecommendation(chat_id = chat_id, item = item)

    # send recommendation to telegram
    send_telegram_recommendation(config = CONFIG,  telegram_recommendation = telegram_recommendation)
        
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