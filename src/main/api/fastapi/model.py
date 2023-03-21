from recommenders.models.sar import SAR
from model_utils import sar_load
import sys
sys.path.append("..")
from bot_world_config import load_model_config, load_sar_config
import os

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
    

if __name__ == "__main__":
    CONFIG = load_sar_config()
    CONFIG.update(load_model_config())
    model = load_sar_model(CONFIG)
    print("Model Load Success!")
    