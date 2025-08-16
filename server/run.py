from app import createApp
import json
from app.utils import svn

config = json.loads(open('config.json').read())
app = createApp(config)

if __name__ == '__main__':
    app.run(debug=True, port=config['server']['port'], host='0.0.0.0')
