import sys
sys.path.append("..")
from bot_world_config import load_manychat_config

def get_manychat_flow_id(config, by):
    if by == "popularity":
        return config['POPULAR_RECOMMENDATION_FLOW_ID']
    elif by == "user":
        return config['PERSONALIZED_RECOMMEDATION_FLOW_ID']
    elif by == "item":
        return config['PERSONALIZED_RECOMMEDATION_FLOW_ID']
    elif by == "hybrid":
        return config['PERSONALIZED_RECOMMEDATION_FLOW_ID']

if __name__ == "__main__":
    CONFIG = load_manychat_config()
    print("Flow ID:", get_manychat_flow_id(CONFIG, by = "popularity"))