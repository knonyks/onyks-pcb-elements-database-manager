from svn.remote import RemoteClient
from svn.local import LocalClient
import datetime
import threading
import time
from pathlib import Path
import pyaltiumlib


class SVN:

    def __init__(self, url, path, user="", password=""):
        self.path = path
        self.user = user
        self.password = password
        self.url = url
        self.lastUpdate = None
        self.remote = RemoteClient(url, username=user, password=password)
        self.rev = 0
        self.footprints = 0
        self.symbols = 0
        self.thread = None

    def init(self):
        self.remote.checkout(self.path)
        self.local = LocalClient(self.path)

    def pull(self):
        self.local.update(self.path)

    def push(self, files):
        for i in files:
            self.local.add(i)
        now = datetime.datetime.now()
        commitDescription = "Server changes at" + str(now)
        self.local.commit(message=commitDescription)

    def getLastCommitIndexAndDate(self):
        result = {}
        result['rev'] = self.local.info()["commit_revision"]
        result['date'] = self.local.info()["commit_date"]
        return result

    def updateLoop(self):
        while True:
            self.pull()
            if self.getLastCommitIndexAndDate()['rev'] > self.rev or self.rev == 0:
                print('✅ THE SVN HAS BEEN UPDATED!')
                self.rev = self.getLastCommitIndexAndDate()['rev']
                #symbols
                folder = Path(self.path) / 'symbols'
                schlib = [f.name for f in folder.glob('*.SchLib')]
                symbolsCountTemp = 0
                for i in schlib:
                    try:
                        schlib_file = pyaltiumlib.read(str(folder / i))
                        symbolsCountTemp += len(schlib_file.list_parts())
                    except:
                        pass
                self.symbols = symbolsCountTemp
                #footprints
                folder = Path(self.path) / 'footprints'
                pcblib = [f.name for f in folder.glob('*.PcbLib')]
                footprintsCountTemp = 0
                for i in pcblib:
                    try:
                        pcblib_file = pyaltiumlib.read(str(folder / i))
                        footprintsCountTemp += len(pcblib_file.list_parts())
                    except:
                        pass
                self.footprints = footprintsCountTemp
            else:
                print('❌ REPO IS STILL THE SAME')
        

    def startLoop(self):
        self.thread = threading.Thread(target=self.updateLoop)
        self.thread.daemon = True
        self.thread.start()
