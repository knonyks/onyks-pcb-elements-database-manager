from flask import Blueprint, render_template, redirect, url_for
import app.utils.forms as forms
from app.utils.database import countTodaysEntries
from pathlib import Path
from app.utils import files
from flask_socketio import emit

def setRoutes(server):

    @server.app.route('/')
    def index():
        parameters = {}
        parameters['title'] = 'Dashboard'
        return redirect(url_for('dashboard', **parameters))

    @server.app.route('/dashboard')
    def dashboard():
        parameters = {}
        parameters['active_page'] = 'dashboard'
        parameters['title'] = 'Dashboard'
        parameters['componentsDatabaseCount'] = sum([server.models[i].query.count() for i in server.models])
        parameters['componentsDatabaseTodaysCount'] = sum([countTodaysEntries(server.db, server.models[i], 'Europe/Warsaw') for i in server.models])
        # parameters['componentsDatabaseLastAddedPartName'] = models.Components.query.order_by(models.Components.created_at.desc()).first().part_name
        parameters['componentsFootprintsCount'] = server.siteDataFill['footprintsAmount']
        parameters['componentsSymbolsCount'] = server.siteDataFill['symbolsAmount']
        return render_template('dashboard.html', **parameters)

    @server.app.route('/search_components')
    def search_compontents():
        parameters = {}
        parameters['active_page'] = 'search_components'
        parameters['title'] = 'Search components'
        parameters['components'] = server.models['Resistors'].query.all()
        return render_template('search_components.html', **parameters)

    @server.app.route('/settings')
    def settings():
        parameters = {}
        parameters['active_page'] = 'settings'
        parameters['title'] = 'Settings'
        return render_template('settings.html', **parameters)

    @server.app.route('/explorer')
    def explorer():
        parameters = {}
        parameters['active_page'] = 'explorer'
        parameters['title'] = 'Explorer'
        return render_template('explorer.html', **parameters)

    @server.app.route('/how_to_configure')
    def how_to_configure():
        parameters = {}
        parameters['active_page'] = 'how_to_configure'
        parameters['title'] = 'How to configure'
        return render_template('how_to_configure.html', **parameters)

    @server.app.route('/element/create', methods=['GET', 'POST'])
    def element_create():
        form = server.forms['creatingElement']()
        if form.validate_on_submit():
            print(form.category.data)
            print(server.config['database']['categories'][int(form.category.data) - 1])
            new_element = server.models[server.config['database']['categories'][int(form.category.data) - 1]](
                part_name = form.part_name.data,
                manufacturer = form.manufacturer.data,
                description = form.description.data,
                library_ref = form.library_ref.data,
                library_path = form.library_path.data,
                footprint_ref_1 = form.footprint_ref_1.data,
                footprint_path_1 = form.footprint_path_1.data,
                footprint_ref_2 = form.footprint_ref_2.data,
                footprint_path_2 = form.footprint_path_2.data,
                footprint_ref_3 = form.footprint_ref_3.data,
                footprint_path_3 = form.footprint_path_3.data
            )
            server.db.session.add(new_element)
            server.db.session.commit()
            
        parameters = {}
        parameters['active_page'] = 'create_element'
        parameters['title'] = 'Create element'
        parameters['form'] = form
        return render_template('element_form.html', **parameters)

def setSocketioRoutes(server):

    @server.socketio.on('explorer-get-files')
    def explorerGetFiles(msg):
        result = files.listFilesWithType(Path('.cache') / msg['path'])
        for i in result:
            if i[0].startswith('.'):
                result.remove(i)
        emit('explorer-files', result)