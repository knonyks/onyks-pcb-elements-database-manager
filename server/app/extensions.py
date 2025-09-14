from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import secrets
from .utils.svn import SVN
from .utils.database import postgresURI
import copy
from .models import getElementModel, getUserModel
from .utils import files
import pyaltiumlib
from pathlib import Path
import time
import threading
import logging
from .routes import setRoutes, setSocketioRoutes
from .utils.forms import getCreatingElementForm, getLoginForm, getChangeUserDataForm, getAddUserForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

class OnyksApp:

    def __init__(self):
        #flask
        self.app = Flask(__name__)

        #database
        self.db = SQLAlchemy()

        #socketio
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        #svn
        self.repository = None
        self.repositoryUpdaterThread = None

        #config's data
        self.config = None
        
        #models
        self.models = {}

        #forms
        self.forms = {}
        self.siteDataFill = {}

        #users
        self.loginManager = None
        self.bcrypt = None

    def __initUsers(self):
        if self.config['database']['usersEnabled']:
            self.bcrypt = Bcrypt(self.app)
            self.loginManager = LoginManager()
            self.loginManager.init_app(self.app)
            self.loginManager.login_view = "login"
            self.loginManager.login_message_category = "info"
            self.models['User'] = getUserModel(self.db, self.config['database']['usersName'])
            
    def __initDatabase(self):
        if self.config['server']['randomizeSecretKey']:
            self.app.config['SECRET_KEY'] = secrets.token_hex(24)
        else:
            self.app.config['SECRET_KEY'] = self.config['server']['secretKey']
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = postgresURI(**self.config['database']['elements'])
        self.db.init_app(self.app)

        for i in self.config['database']['categories']:
            self.models[i] = getElementModel(self.db, i)

    def __initRepository(self):
        configCopy = copy.deepcopy(self.config['svn']['config'])
        configCopy['path'] = './.cache/svn'
        self.repository = SVN(**configCopy)
        self.repository.init()
        self.repository.pull()
        self.repositoryUpdaterThread = threading.Thread(target = self.__repositoryUpdater)
        self.repositoryUpdaterThread.deamon = True
        self.repositoryUpdaterThread.start()

    def __initSiteDataFill(self):
        self.siteDataFill["symbolsAmount"] = 0
        self.siteDataFill["footprintsAmount"] = 0

    def __repositoryUpdater(self):
        symbolsPath = Path(self.repository.path) / self.config['svn']['source_folders']['symbols']
        footprintsPath = Path(self.repository.path) / self.config['svn']['source_folders']['footprints']
        rev = 0

        while True:
            result = self.__detectRepositoryUpdate(symbolsPath.as_posix(), footprintsPath.as_posix(), rev)
            if result != None:
                # print(result)
                self.siteDataFill["symbolsAmount"] = result[0]
                self.siteDataFill["footprintsAmount"] = result[1]
                rev = result[2]
                # print(symbolsAmount, footprintsAmount, rev)
                # self.socketio.emit('update', {'source':'svn', 'content': [symbolsAmount, footprintsAmount, rev]})
            else:
                pass
            time.sleep(self.config['svn']['update_frequency'])

    def __detectRepositoryUpdate(self, symbolsPath, footprintsPath, lastRev):
        self.repository.local.cleanup()
        self.repository.pull()


        if self.repository.getLastCommitIndexAndDate()['rev'] > lastRev or lastRev == 0:
            print('✅ THE SVN HAS BEEN UPDATED!')

            #rev
            rev = self.repository.getLastCommitIndexAndDate()['rev']

            #symbols
            paths = files.findAllFiles(symbolsPath, '.SchLib')
            symbols = 0
            for i in paths:
                try:
                    schlib_file = pyaltiumlib.read(i)
                    symbols += len(schlib_file.list_parts())
                except:
                    pass

            #footprints
            paths = files.findAllFiles(footprintsPath, '.PcbLib')
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
        
    def __initForms(self):
        self.forms['creatingElement'] = getCreatingElementForm(self.config['database']['categories'])
        if self.config['database']['usersEnabled']:
            self.forms['loginForm'] = getLoginForm()
            self.forms['changeUserDataForm'] = getChangeUserDataForm()
            self.forms['addUserForm'] = getAddUserForm()

    def __initRoutes(self):
        setRoutes(self)
        setSocketioRoutes(self)

    def init(self, config):
        self.config = config

        self.__initSiteDataFill()
        self.__initDatabase()
        self.__initUsers()
        self.__initRepository()
        self.__initForms()
        self.__initRoutes()

    def run(self):
        self.socketio.run(self.app, debug = True, port = self.config['server']['port'], host = '0.0.0.0')