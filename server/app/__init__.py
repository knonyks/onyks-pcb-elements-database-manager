from flask import Flask
from app.utils import database
from flask_sqlalchemy import SQLAlchemy
from app.utils import svn
import pprint
import pyaltiumlib

db = SQLAlchemy()
repo = None


def createApp(config):
    global repo, db
    app = Flask(__name__)

    #CONFIG DATABASE
    app.config['SQLALCHEMY_DATABASE_URI'] = database.createPostgresURI(**config['compontentsDatabase'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    repo = svn.SVN(**config['svn'])
    repo.init()
    repo.pull()
    repo.startLoop()

    #SET SERVER BEHAVIOUR
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app