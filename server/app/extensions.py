from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import secrets
from .utils.svn import SVN
from .utils.database import postgresURI
import copy
from .models import createElementsTable
from .utils import files
import pyaltiumlib
from pathlib import Path
import time
import threading
import logging
from .routes import mainRoutes, socketioRoutes

class OnyksApp:

    def __init__(self):
        self.app = Flask(__name__)
        self.db = SQLAlchemy()
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.repository = None
        self.config = None
        self.tables = {}
        self.others = {}
        self.repositoryUpdaterThread = None

    def __initDatabase(self):
        self.app.config['SECRET_KEY'] = secrets.token_hex(24)
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        configCopy = copy.deepcopy(self.config['database'])
        configCopy.pop('usersTableEnabled')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = postgresURI(**configCopy['connection'])

        self.db.init_app(self.app)

    def __initRepository(self):
        configCopy = copy.deepcopy(self.config['svn']['config'])
        configCopy['path'] = './.cache/svn'
        self.repository = SVN(**configCopy)
        self.repository.init()
        self.repository.pull()
        self.repositoryUpdaterThread = threading.Thread(target = self.__repositoryUpdater)
        self.repositoryUpdaterThread.deamon = True
        self.repositoryUpdaterThread.start()

    def __createTables(self):
        self.tables['Components'] = createElementsTable(self.db, 'Components')

    def __initOthers(self):
        self.others["symbolsAmount"] = 0
        self.others["footprintsAmount"] = 0

    def __repositoryUpdater(self):
        symbolsPath = Path(self.repository.path) / self.config['svn']['source_folders']['symbols']
        footprintsPath = Path(self.repository.path) / self.config['svn']['source_folders']['footprints']
        rev = 0

        while True:
            result = self.__detectRepositoryUpdate(symbolsPath.as_posix(), footprintsPath.as_posix(), rev)
            if result != None:
                # print(result)
                self.others["symbolsAmount"] = result[0]
                self.others["footprintsAmount"] = result[1]
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

    def __initRoutes(self):
        mainRoutes(self)
        socketioRoutes(self)

    def init(self, config):
        self.config = config
        self.__initOthers()
        self.__initDatabase()
        self.__initRepository()
        self.__createTables()
        self.__initRoutes()



    def run(self):
        self.socketio.run(server.app, debug=True, port=self.config['server']['port'], host='0.0.0.0')

server = OnyksApp()