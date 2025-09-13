import json
import argparse
from app.extensions import OnyksApp

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="config.json", help="A server config's path")
args = parser.parse_args()

config = json.loads(open(args.config).read())
server = OnyksApp()
server.init(config)

if __name__ == '__main__':
    server.run()