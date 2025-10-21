from apscheduler.schedulers.background import BackgroundScheduler
import redis, json, time
import argparse, copy
from datetime import datetime
from pathlib import Path
import app.utils.files as files
import pyaltiumlib
import os
from app.utils.svn import SVN

#config loading
# parser = argparse.ArgumentParser()
# parser.add_argument("--config", type=str, default="config.json", help="A server config's path")
# args = parser.parse_args()


config_path = os.environ.get("ONYKS_CONFIG", "config.json")
config = json.loads(open(config_path).read())

config_copy = copy.deepcopy(config['svn']['config'])
config_copy['path'] = Path('.cache') / Path('svn')
config_copy['path'] = str(config_copy['path'])

#redis init
r = redis.Redis(host="localhost", port=6379, db=0)

#repository init
repository = SVN(**config_copy)
rev = 0
repository.init()
repository.pull()
symbols_path = Path(repository.path) / config['svn']['source_folders']['symbols']
footprints_path = Path(repository.path) / config['svn']['source_folders']['footprints']

symbols_amount = 0
footprints_amount = 0

r.set("symbols_amount", 0)
r.set("footprints_amount", 0)

def __detect_repository_update(symbols_path, footprints_path, last_rev):
    global repository, rev, r, config
    print(repository)
    repository.local.cleanup()
    repository.pull()

    print(repository.getLastCommitIndexAndDate()['rev'] > last_rev or last_rev == 0)
    if repository.getLastCommitIndexAndDate()['rev'] > last_rev or last_rev == 0:
        #rev
        rev = repository.getLastCommitIndexAndDate()['rev']

        #symbols
        paths = files.findAllFiles(symbols_path, '.SchLib')
        symbols = 0
        for i in paths:
            try:
                schlib_file = pyaltiumlib.read(i)
                symbols += len(schlib_file.list_parts())
                print("adsad", len(schlib_file.list_parts()))
            except Exception as e:
                print("Error reading symbol file:", i, e)

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
        return None

def repository_updater():
    global repository, rev, r, symbols_path, footprints_path
    result = __detect_repository_update(symbols_path.as_posix(), footprints_path.as_posix(), rev)
    if result != None:
        print("sss", result)
        symbols_amount = result[0]
        footprints_amount = result[1]
        r.set("symbols_amount", symbols_amount)
        r.set("footprints_amount", footprints_amount)
        rev = result[2]

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(repository_updater, "interval", seconds = 1)
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()