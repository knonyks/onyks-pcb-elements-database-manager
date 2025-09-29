from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import secrets
from .utils.svn import SVN
from .utils.database import postgres_URI
import copy
from .models import get_element_model, get_user_model
from .utils import files
import pyaltiumlib
from pathlib import Path
import time
import threading
import logging
from .routes import set_routes, set_socketio_routes
from .utils.forms import get_creating_element_form, get_login_form, get_change_user_data_form, get_add_user_form
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import signal, sys
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
import os

class Models:

    def __init__(self):
        self.user = None
        self.categories = {}

class Engines:

    def __init__(self):
        self.user = None
        self.categories = None

class OnyksApp:

    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        self.db = SQLAlchemy()
        self.config = None
        self.models = Models()
        self.engines = Engines()
        self.filling_site_data = {}
        self.login_manager = None
        self.bcrypt = None

        #svn
        self.repository = None
        self.repository_updater_flag = True
        self.repository_updater_thread = None

        #forms
        self.forms = {}
        
    def __init_filling_site_data(self):
        self.filling_site_data["symbols_amount"] = 0
        self.filling_site_data["footprints_amount"] = 0

    def __init_database(self):
        #SET UP THE SECRET KEY
        if self.config['server']['randomize_secret_key']:
            self.app.config['SECRET_KEY'] = secrets.token_hex(24)
        else:
            self.app.config['SECRET_KEY'] = self.config['server']['secret_key']

        #ELEMENTS
        self.app.config['SQLALCHEMY_DATABASE_URI'] = postgres_URI(**self.config['database']['elements']['settings'])

        #USERS
        if self.config['database']['users']['is_enabled']:
            self.bcrypt = Bcrypt(self.app)
            self.login_manager = LoginManager()
            self.login_manager.init_app(self.app)
            self.login_manager.login_view = "login"
            self.login_manager.login_message_category = "info"
            self.app.config["SQLALCHEMY_BINDS"] = {}
            self.app.config["SQLALCHEMY_BINDS"]["users"] = postgres_URI(**self.config['database']['users']['settings'])
            self.models.user = get_user_model(self.db, "users", self.config["database"]["users"]["table_name"])

        #OTHERS
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db.init_app(self.app)

        #ELEMENTS
        for i in self.config['database']['elements']['categories_tables_name']:
            self.models.categories[i] = get_element_model(self.db, i)

    def __init_repository(self):
        config_copy = copy.deepcopy(self.config['svn']['config'])
        config_copy['path'] = Path('.cache') / Path('svn')
        config_copy['path'] = str(config_copy['path'])
        self.repository = SVN(**config_copy)

        self.repository.init()
        self.repository.pull()

        self.repository_updater_thread = threading.Thread(target = self.__repository_updater)
        self.repository_updater_thread.deamon = True
        self.repository_updater_thread.start()

    def __repository_updater(self):
        symbols_path = Path(self.repository.path) / self.config['svn']['source_folders']['symbols']
        footprints_path = Path(self.repository.path) / self.config['svn']['source_folders']['footprints']
        rev = 0

        while self.repository_updater_flag:
            result = self.__detect_repository_update(symbols_path.as_posix(), footprints_path.as_posix(), rev)
            if result != None:
                self.filling_site_data["symbols_amount"] = result[0]
                self.filling_site_data["footprints_amount"] = result[1]
                rev = result[2]
            else:
                pass
            if not self.repository_updater_flag:
                break
            time.sleep(self.config['svn']['update_frequency'])
        print("❌❌❌  SVN LOOP ENDS!!  ❌❌❌")

    def __detect_repository_update(self, symbols_path, footprints_path, last_rev):
        self.repository.local.cleanup()
        self.repository.pull()


        if self.repository.getLastCommitIndexAndDate()['rev'] > last_rev or last_rev == 0:
            print('✅ THE SVN HAS BEEN UPDATED!')

            #rev
            rev = self.repository.getLastCommitIndexAndDate()['rev']

            #symbols
            paths = files.findAllFiles(symbols_path, '.SchLib')
            symbols = 0
            for i in paths:
                try:
                    schlib_file = pyaltiumlib.read(i)
                    symbols += len(schlib_file.list_parts())
                except:
                    pass

            #footprints
            paths = files.findAllFiles(footprints_path, '.PcbLib')
            footprints = 0
            for i in paths:
                try:
                    schlib_file = pyaltiumlib.read(i)
                    footprints += len(schlib_file.list_parts())
                except:
                    pass
            return symbols, footprints, rev
        else:
            print('❌ THE SVN HASN\'T HAD AN UPDATE!')
            return None
        
    def __init_forms(self):
        self.forms['creating_element'] = get_creating_element_form(self.config['database']['elements']['categories_tables_name'])
        if self.config['database']['users']['is_enabled']:
            self.forms['login'] = get_login_form()
            self.forms['change_user_data'] = get_change_user_data_form()
            self.forms['add_user'] = get_add_user_form()

    def __init_routes(self):
        set_routes(self)
        set_socketio_routes(self)

    def __signal_exit(self, signum, frame):
        print("❌❌❌  APP IS CLOSING!!  ❌❌❌")
        self.repository_updater_flag = False
        sys.exit(0)

    def init(self, config):
        self.config = config

        self.app.config['UPLOAD_FOLDER'] = os.path.abspath(config['database']['elements']['datasheets_folder_path'])

        self.__init_filling_site_data()
        self.__init_database()
        self.__init_repository()
        self.__init_forms()
        self.__init_routes()

        signal.signal(signal.SIGINT, self.__signal_exit)
        signal.signal(signal.SIGTERM, self.__signal_exit)

    def run(self):
        self.socketio.run(self.app, debug = True, port = self.config['server']['port'], host = '0.0.0.0')