import sys
sys.path.append("..")
from model_utils import sar_load
from bot_world_config import load_model_config, load_sar_config, load_session_config
from bot_world_classes import RecommendRequest

import os
import pandas as pd
from math import ceil
from recommenders.models.sar import SAR

RUNNING_LOCALLY = os.environ.get("USERNAME","unknown") =="tanch"

def load_sar_model(config): 
    model = SAR(
        col_user=config['COL_USER'],
        col_item=config['COL_ITEM'],
        col_rating=config['COL_RATING'],
        similarity_type=config['SIMILARITY_TYPE'], 
        time_decay_coefficient=30, 
        timedecay_formula=False,
        normalize=False
    )
    sar_load(model, config['MODEL_DIR'] if not RUNNING_LOCALLY else r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\api\models\arietes-sar")
    return model

def predict(config, model, recommend_request: RecommendRequest):

    recommended_item_ids = []
    
    if recommend_request.by == "user":
        model_output = model.recommend_k_items(
            test = pd.DataFrame({config["COL_USER"]:[recommend_request.user_id]}), 
            top_k=config["SESSION_RECOMMENDATION_SIZE"], 
            remove_seen=True
            )
        recommended_item_ids = model_output[config["COL_ITEM"]].tolist()

    elif recommend_request.by == "item":
        model_output = model.get_item_based_topk(
            items = pd.DataFrame({config["COL_ITEM"]:[recommend_request.item_id]}), 
            top_k=config["SESSION_RECOMMENDATION_SIZE"]
            )
        recommended_item_ids = model_output[config["COL_ITEM"]].tolist()

    elif recommend_request.by == "popularity":
        model_output = model.get_popularity_based_topk(top_k=config["SESSION_RECOMMENDATION_SIZE"])
        recommended_item_ids = model_output[config["COL_ITEM"]].tolist()

    elif recommend_request.by =="hybrid":
        model_output_popularity_based = model.get_popularity_based_topk(top_k=config["SESSION_RECOMMENDATION_SIZE"])
        recommended_item_ids.extend(model_output_popularity_based[config["COL_ITEM"]].tolist()[:ceil(config["SESSION_RECOMMENDATION_SIZE"]/2)])
        model_output_user_based = model.recommend_k_items(
            test = pd.DataFrame({config["COL_USER"]:[recommend_request.user_id]}), 
            top_k=config["SESSION_RECOMMENDATION_SIZE"]//2, 
            remove_seen=True
            )
        recommended_item_ids.extend(model_output_user_based[config["COL_ITEM"]].tolist())

    return recommended_item_ids

if __name__ == "__main__":
    CONFIG = load_sar_config()
    CONFIG.update(load_model_config())
    CONFIG.update(load_session_config())
    MODEL = load_sar_model(CONFIG)
    print("Model Load Success!")

    recommend_request = RecommendRequest(by = "popularity")
    predictions = predict(CONFIG, MODEL, recommend_request)
    print(f"Predictions: {predictions}")

    recommend_request = RecommendRequest(user_id = "bignphat",by = "user")
    predictions = predict(CONFIG, MODEL, recommend_request)
    print(f"Predictions: {predictions}")

    recommend_request = RecommendRequest(user_id = "bignphat",by = "hybrid")
    predictions = predict(CONFIG, MODEL, recommend_request)
    print(f"Predictions: {predictions}")

    recommend_request = RecommendRequest(item_id = "13950585519",by = "item")
    predictions = predict(CONFIG, MODEL, recommend_request)
    print(f"Predictions: {predictions}")
    print("Model Predict Success!")
