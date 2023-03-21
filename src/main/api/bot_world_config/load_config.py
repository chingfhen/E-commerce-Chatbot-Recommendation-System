import yaml
import os

IN_DOCKER = not os.environ.get("USERNAME","unknown") =="tanch"

if IN_DOCKER:    

    def load_database_config():
        with open(os.path.join(os.environ.get("CONFIG_DIR"),"database-config.yaml"), "r") as f:
            return yaml.safe_load(f)
    def load_model_config():
        with open(os.path.join(os.environ.get("CONFIG_DIR"),"model-config.yaml"), "r") as f:
            return yaml.safe_load(f)
    def load_sar_config():
        with open(os.path.join(os.environ.get("CONFIG_DIR"),"sar-config.yaml"), "r") as f:
            return yaml.safe_load(f)
    def load_seller_config():
        with open(os.path.join(os.environ.get("CONFIG_DIR"),"seller-config.yaml"), "r") as f:
            return yaml.safe_load(f)
    def load_session_config():
        with open(os.path.join(os.environ.get("CONFIG_DIR"),"session-config.yaml"), "r") as f:
            return yaml.safe_load(f)
    def load_telegram_bot_config():
        with open(os.path.join(os.environ.get("CONFIG_DIR"),"telegram-bot-config.yaml"), "r") as f:
            return yaml.safe_load(f)

else:     
    def load_database_config():
        with open(r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\api\bot_world_config\database-config.yaml", "r") as f:
            return yaml.safe_load(f)
    def load_model_config():
        with open(r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\api\bot_world_config\model-config.yaml", "r") as f:
            return yaml.safe_load(f)
    def load_sar_config():
        with open(r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\api\bot_world_config\sar-config.yaml", "r") as f:
            return yaml.safe_load(f)
    def load_seller_config():
        with open(r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\api\bot_world_config\seller-config.yaml", "r") as f:
            return yaml.safe_load(f)
    def load_session_config():
        with open(r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\api\bot_world_config\session-config.yaml", "r") as f:
            return yaml.safe_load(f)
    def load_telegram_bot_config():
        with open(r"C:\Users\tanch\Desktop\Bot.World\Bot.World\src\main\api\bot_world_config\telegram-bot-config.yaml", "r") as f:
            return yaml.safe_load(f)    