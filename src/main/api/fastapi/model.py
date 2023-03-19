# sar
from recommenders.models.sar import SAR
from model_utils import sar_load

import yaml
import os



"""
This script will load the chosen recommendation model
"""
# load configurations
local_path = r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\config\model-config.yaml"
volume_path = "/config/model-config.yaml"
config_path = local_path if os.path.exists(local_path) else volume_path
with open(config_path, "r") as f:
    try:
        model_config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

# check if the model is supported
if model_config["MODEL_TYPE"] not in model_config["MODEL_SUPPORTED_TYPES"]:
    raise ValueError("'MODEL' not recognized")
    
# load specific model configurations
if model_config["MODEL_TYPE"]=="sar":
    local_path = r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\config\sar-config.yaml"
    volume_path = "/config/sar-config.yaml"
    config_path = local_path if os.path.exists(local_path) else volume_path
elif model_config["MODEL_TYPE"]=="lightgcn":
    raise ValueError("Oops Something went Wrong!")
with open(config_path, "r") as f:
    try:
        model_config.update(yaml.safe_load(f))
    except yaml.YAMLError as exc:
        print(exc)

# load the specific model
if model_config["MODEL_TYPE"]=="sar":
    local_path = r"C:\Users\tanch\Documents\NTU\NTU Year 4\FYP - GNN\Recommender API\deploy-fastapi-recommendation-system\src\api\models\arietes-sar"
    model_path = local_path if os.path.exists(local_path) else model_config['MODEL_DIR']
    model = SAR(
        col_user=model_config['COL_USER'],
        col_item=model_config['COL_ITEM'],
        col_rating=model_config['COL_RATING'],
        similarity_type=model_config['SIMILARITY_TYPE'], 
        time_decay_coefficient=30, 
        timedecay_formula=False,
        normalize=False
    )
    sar_load(model, model_path)

elif model_config["MODEL_TYPE"]=="lightgcn":
    raise ValueError("Oops Something went Wrong!")
    

if __name__ == "__main__":
    print("Done")
    