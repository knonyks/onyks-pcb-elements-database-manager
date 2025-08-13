from flask import Blueprint, render_template, redirect, url_for
from app import models
from app import repo
from app.utils.database import countTodaysEntries

main_bp = Blueprint('main', __name__)

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
    parameters['componentsDatabaseTodaysCount'] = countTodaysEntries('Europe/Warsaw')
    parameters['componentsDatabaseLastAddedPartName'] = models.Components.query.order_by(models.Components.created_at.desc()).first().part_name
    parameters['componentsFootprintsCount'] = repo.footprints
    parameters['componentsSymbolsCount'] = repo.symbols
    return render_template('dashboard.html', **parameters)

@main_bp.route('/search_components', methods=['GET', 'POST'])
def search_compontents():
    parameters = {}
    parameters['title'] = 'Search components'
    parameters['components'] = models.Components.query.all()
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