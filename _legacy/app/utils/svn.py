from svn.remote import RemoteClient
from svn.local import LocalClient
import datetime
import threading
import time
from pathlib import Path
import pyaltiumlib
from app.utils.files import findAllFiles

class SVN:

    def __init__(self, url, path, user="", password=""):
        self.path = path
        self.user = user
        self.password = password
        self.url = url
        self.remote = RemoteClient(url, username=user, password=password)

    def init(self):
        self.remote.checkout(self.path)
        self.local = LocalClient(self.path, username=self.user, password=self.password)
        self.local.cleanup()

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

    def startLoop(self):
        pass
        self.thread = threading.Thread(target=self.updateLoop)
        self.thread.daemon = True
        self.thread.start()


def svnUpdateDetect(svn_repo, symbolsPath, footprintsPath, last_rev):
    svn_repo.local.cleanup()
    svn_repo.pull()
    if svn_repo.getLastCommitIndexAndDate()['rev'] > last_rev or last_rev == 0:
        print('✅ THE SVN HAS BEEN UPDATED!')

        #rev
        rev = svn_repo.getLastCommitIndexAndDate()['rev']

        #symbols
        paths = findAllFiles(symbolsPath, '.SchLib')
        symbols = 0
        for i in paths:
            try:
                schlib_file = pyaltiumlib.read(i)
                symbols += len(schlib_file.list_parts())
            except:
                pass

        #footprints
        paths = findAllFiles(footprintsPath, '.PcbLib')
        footprints = 0
        for i in paths:
            try:
                schlib_file = pyaltiumlib.read(i)
                footprints += len(schlib_file.list_parts())
            except:
                pass
        return symbols, footprints, rev
    else:
        return None