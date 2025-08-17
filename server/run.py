from app import createApp
import json
from app.utils import svn
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="config.json", help="A server config's path")
args = parser.parse_args()

config = json.loads(open(args.config).read())
app, socketio = createApp(config)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=config['server']['port'], host='0.0.0.0')
