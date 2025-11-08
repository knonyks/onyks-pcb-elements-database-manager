from app import models
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from zoneinfo import ZoneInfo
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date, datetime

def postgres_URI(username, password, host, name, port):
    addr = 'postgresql://'
    addr += username
    addr += ':'
    addr += password
    addr += '@' + host + ":" + str(port) + '/'
    addr += name
    return addr

def count_todays_entries(model):
    today = date.today()
    count_today = model.query.filter(
        model.created_at >= datetime(today.year, today.month, today.day)
    ).count()
    return count_today

def last_entry(models):
    last_entries = []
    for i in models:
        last_entries.append(i.query.order_by(i.created_at.desc()).first())
    latest_entry = max(last_entries, key=lambda x: x.created_at if x else datetime.min)
    return latest_entry


def find_uuid_in_selected_models(uuid_value, models):
    results = []

    for model in models:
        # upewniamy się, że to model z tabelą
        if hasattr(model, '__table__'):
            # sprawdzamy czy model ma kolumnę 'uuid'
            if 'uuid' in model.__table__.columns:
                rows = model.query.filter_by(uuid=uuid_value).all()
                if rows:
                    results.append((model.__tablename__, rows))

    return results