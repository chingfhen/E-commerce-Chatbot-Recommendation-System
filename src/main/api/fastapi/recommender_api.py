import json
from fastapi import FastAPI
import uvicorn

import sys
sys.path.append("..")
from bot_world_config import *
from db import establish_database_connection, get_products
from model import load_sar_model, predict
from bot_world_classes import *
from session import load_session, get_session_id




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
    
    recommended_item_ids = predict(CONFIG, global_model, recommend_request)
    
    return {"recommendations": recommended_item_ids}

"""
Documentation
"""
@app.post("/manychat/recommend")
async def manychat_recommend(chat_id: int, recommend_request: RecommendRequest):
    
    ID = get_session_id(chat_id = chat_id, by = recommend_request.by, user_id = recommend_request.user_id, item_id = recommend_request.item_id)

    # if session doesn't exist, then make a model and database call
    if not global_session.exists(ID = ID):

        # MODEL CALL
        recommended_item_ids = predict(CONFIG, global_model, recommend_request)

        # DATABASE CALL
        products = get_products(CONFIG, global_database_connection, recommended_item_ids)   

        # add to session
        global_session.add(ID = ID, recommendations = products) 

    # retrieve 1 recommendation from session
    item = global_session.recommend(ID = ID)
        
    return {
        "version": "v2",
        "content": {
            "type":"telegram",
            "messages": [
                {
                    "type": "image",
                    "url": item.image_url
                },
                {
                    "type": "text",
                    "text": item.product_name,
                    "buttons": [
                        {
                            "type": "flow",
                            "caption": "Next",
                            "target": "content20230329055930_635372"
                        },
                        {
                            "type": "url",
                            "caption": "Purchase",
                            "url": f"https://shopee.sg/product/{CONFIG['SELLER_ID']}/{item.product_id}",
                            "webview_size": "full"
                        }
                    ]
                }
            ]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)