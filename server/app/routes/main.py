from flask import Blueprint, render_template, redirect, url_for
from app import models
from app import db
from app import repo
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Wbudowane w Python 3.9+
from sqlalchemy import func, and_

main_bp = Blueprint('main', __name__)

from datetime import datetime, timedelta
from pytz import timezone

def count_todays_entries(timezone_str: str = 'Europe/Warsaw') -> int:
    user_tz = ZoneInfo(timezone_str)
    now_local = datetime.now(user_tz)
    
    start_of_day = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    start_utc = start_of_day.astimezone(ZoneInfo('UTC'))
    end_utc = end_of_day.astimezone(ZoneInfo('UTC'))
    
    return db.session.query(
        func.count(models.Components.uuid)
    ).filter(
        and_(
            models.Components.created_at >= start_utc,
            models.Components.created_at < end_utc
        )
    ).scalar() or 0

@main_bp.route('/')
def index():
    parameters = {}
    parameters['title'] = 'Dashboard'
    return redirect(url_for('main.dashboard', **parameters))

@main_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    parameters = {}
    parameters['title'] = 'Dashboard'
    parameters['componentsDatabaseCount'] = models.Components.query.count()
    x = count_todays_entries('Europe/Warsaw')
    parameters['componentsDatabaseTodaysCount'] = x
    parameters['componentsDatabaseLastAddedPartName'] = models.Components.query.order_by(models.Components.created_at.desc()).first().part_name
    parameters['componentsFootprintsCount'] = repo.footprints
    parameters['componentsSymbolsCount'] = repo.symbols
    return render_template('dashboard.html', **parameters)

@main_bp.route('/search_components', methods=['GET', 'POST'])
def search_compontents():
    parameters = {}
    parameters['title'] = 'Search components'
    return render_template('search_components.html', **parameters)

@main_bp.route('/symbols', methods=['GET', 'POST'])
def symbols():
    parameters = {}
    parameters['title'] = 'Symbols'
    return render_template('symbols.html', **parameters)

@main_bp.route('/footprints', methods=['GET', 'POST'])
def footprints():
    parameters = {}
    parameters['title'] = 'Footprints'
    return render_template('footprints.html', **parameters)

@main_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    parameters = {}
    parameters['title'] = 'Settings'
    return render_template('settings.html', **parameters)