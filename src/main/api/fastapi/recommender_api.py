

import pandas as pd
import json
from fastapi import FastAPI
import yaml
import os
from db import database_config, database_connection, database_cursor, get_product_info
from model import model_config, model
from bot_world_classes import Query, Product, SessionRecommendations
from telegram_bot_messages import send_recommendation
from session import session_config, session

# CREATE SESSION

# load config
config = {}
config.update(database_config)
config.update(model_config)
config.update(session_config)



local_path = r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\config\seller-config.yaml"
volume_path = "/config/seller-config.yaml"
config_path = local_path if os.path.exists(local_path) else volume_path
with open(config_path, "r") as f:
    try:
        config.update(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)


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
    model_output = model.recommend_k_items(pd.DataFrame({"user_id":[query.user_id]}), top_k=config["SESSION_RECOMMENDATION_SIZE"], remove_seen=True)
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

    if not session.exists(query.user_id):
        # call the model
        model_output = model.recommend_k_items(pd.DataFrame({"user_id":[query.user_id]}), top_k=config["SESSION_RECOMMENDATION_SIZE"], remove_seen=True)
        item_ids = list(map(int, model_output[config["COL_ITEM"]].tolist()))
        # call the database
        products = get_products(database_cursor, item_ids)    
        # add to session
        session.add(user_id = query.user_id, recommendations = products)
    
    item = session.recommend(user_id = query.user_id)

    send_recommendation(query.chat_id, item)
    
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

if __name__=="__main__":
    # product_id, product_name, categories, image_url = get_product_info(database_cursor, 23821143235)
    # print(product_id, product_name, categories, image_url )
    print("Done")



# read environment variables
# DATABASE_FOLDER = os.environ.get('DATABASE_FOLDER')
# DATABASE_NAME = os.environ.get('DATABASE_NAME')

# # establish database connection
# database_connection = sqlite3.connect(f"{DATABASE_DIR}/{DATABASE_NAME}.db" if DATABASE_FOLDER is not None else "/database/sqlite3/arietes_product_info.db")
# database_cursor = database_connection.cursor()

# manychat endpoints
# manychat_router = APIRouter()
# app.include_router(manychat_recommender.manychat_router)





