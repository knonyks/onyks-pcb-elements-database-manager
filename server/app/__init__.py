from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.utils import svn

db = SQLAlchemy()
repo = None


def createApp(config):
    global repo, db

    from app.utils.database import createPostgresURI

    app = Flask(__name__)

    #CONFIG DATABASE
    app.config['SQLALCHEMY_DATABASE_URI'] = createPostgresURI(**config['compontentsDatabase'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #CONFIG SVN
    repo = svn.SVN(**config['svn'])
    repo.init()
    repo.pull()
    repo.startLoop()

    #SET SERVER BEHAVIOUR
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app