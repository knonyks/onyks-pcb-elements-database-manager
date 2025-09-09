from app import socketio
from pathlib import Path
from app.utils import files
from flask_socketio import SocketIO, send, emit


@socketio.on('explorer-get-files')
def handle_message(msg):
    result = files.listFilesWithType(Path('.cache') / msg['path'])

    for i in result:
        if i[0].startswith('.'):
            result.remove(i)
    emit('explorer-files', result)



