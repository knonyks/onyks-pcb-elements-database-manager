# from flask import Flask, render_template, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from app.utils import svn
# import threading
# from flask_socketio import SocketIO, emit
# import time
# from pathlib import Path
# from app.utils import images
# from flask_wtf import FlaskForm
# from wtforms import StringField, TextAreaField, SubmitField
# from wtforms.validators import DataRequired, Length
# import os
# import secrets

# db = SQLAlchemy()
# repo = None
# socketio = None

# svnUpdaterThread = None
# footprintsAmount = 0
# symbolsAmount = 0
# revRepo = 0

# def createApp(config):
#     global repo, db, socketio

#     from app.utils.database import createPostgresURI

#     app = Flask(__name__)
#     socketio = SocketIO(app, cors_allowed_origins="*")

#     #CONFIG DATABASE
#     app.config['SECRET_KEY'] = secrets.token_hex(24)
#     app.config['SQLALCHEMY_DATABASE_URI'] = createPostgresURI(**config['elementsDatabase'])
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)

#     #CONFIG SVN
#     config['svn']['config']['path'] = './.cache/svn'
#     repo = svn.SVN(**config['svn']['config'])
#     repo.init()
#     repo.pull()

#     def svnThread():
#         global symbolsAmount, footprintsAmount, revRepo
#         symbolsPath = Path(repo.path) / config['svn']['source_folders']['symbols']
#         footprintsPath = Path(repo.path) / config['svn']['source_folders']['footprints']
#         while True:
#             result = svn.svnUpdateDetect(repo, symbolsPath.as_posix(), footprintsPath.as_posix(), revRepo)
            
#             if result != None:
#                 print(result)
#                 symbolsAmount = result[0]
#                 footprintsAmount = result[1]
#                 revRepo = result[2]
#                 print(symbolsAmount, footprintsAmount, revRepo)
#                 socketio.emit('update', {'source':'svn', 'content': [symbolsAmount, footprintsAmount, revRepo]})
#             else:
#                 pass
#             time.sleep(config['svn']['update_frequency'])


#     #SVN UPDATER
#     svnUpdaterThread = threading.Thread(target = svnThread)
#     svnUpdaterThread.deamon = True
#     svnUpdaterThread.start()

#     #SET SERVER BEHAVIOUR
#     from app.routes.main import main_bp
#     app.register_blueprint(main_bp)
#     import app.routes.explorer as explorer

#     images.createDatabaseConfigImage(config['elementsDatabase'], 'app/static/img/windows_odbc_form.png', 'app/static/.cache/windows_odbc_filled_form.png')

#     return app, socketio

