from app import db
from app import models
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from zoneinfo import ZoneInfo

def createPostgresURI(username, password, host, name, port):
    addr = 'postgresql://'
    addr += username
    addr += ':'
    addr += password
    addr += '@' + host + ":" + str(port) + '/'
    addr += name
    return addr

def countTodaysEntries(timezone_str = 'Europe/Warsaw'):
    user_tz = ZoneInfo(timezone_str)
    now_local = datetime.now(user_tz)
    
    start_of_day = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    start_utc = start_of_day.astimezone(ZoneInfo('UTC'))
    end_utc = end_of_day.astimezone(ZoneInfo('UTC'))
    
    return db.session.query(func.count(models.Components.uuid)).filter \
    (
        and_ \
        (
            models.Components.created_at >= start_utc,
            models.Components.created_at < end_utc
        )
    ).scalar() or 0