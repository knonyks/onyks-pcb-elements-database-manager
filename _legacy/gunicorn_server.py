from app.onyks import OnyksApp
import json
import os

config_path = os.environ.get("ONYKS_CONFIG", "config.json")

config = json.loads(open(config_path).read())
server = OnyksApp()
server.init(config)
app = server.app