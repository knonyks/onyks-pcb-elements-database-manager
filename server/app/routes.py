from flask import Blueprint, render_template, redirect, url_for
import app.utils.forms as forms
from app.utils.database import countTodaysEntries

def mainRoutes(server):

    main_bp = Blueprint('main', __name__)

    @main_bp.route('/')
    def index():
        parameters = {}
        parameters['title'] = 'Dashboard'
        return redirect(url_for('main.dashboard', **parameters))

    @main_bp.route('/dashboard')
    def dashboard():
        parameters = {}
        parameters['active_page'] = 'dashboard'
        parameters['title'] = 'Dashboard'
        parameters['componentsDatabaseCount'] = sum([server.categories[i].query.count() for i in server.categories])
        parameters['componentsDatabaseTodaysCount'] = sum([countTodaysEntries(server.db, server.categories[i], 'Europe/Warsaw') for i in server.categories])
        # parameters['componentsDatabaseLastAddedPartName'] = models.Components.query.order_by(models.Components.created_at.desc()).first().part_name
        parameters['componentsFootprintsCount'] = server.others['footprintsAmount']
        parameters['componentsSymbolsCount'] = server.others['symbolsAmount']
        return render_template('dashboard.html', **parameters)

    @main_bp.route('/search_components')
    def search_compontents():
        parameters = {}
        parameters['active_page'] = 'search_components'
        parameters['title'] = 'Search components'
        parameters['components'] = server.categories['Resistors'].query.all()
        return render_template('search_components.html', **parameters)

    @main_bp.route('/symbols')
    def symbols():
        parameters = {}
        parameters['active_page'] = 'symbols'
        parameters['title'] = 'Symbols'
        return render_template('symbols.html', **parameters)

    @main_bp.route('/footprints')
    def footprints():
        parameters = {}
        parameters['active_page'] = 'footprints'
        parameters['title'] = 'Footprints'
        return render_template('footprints.html', **parameters)

    @main_bp.route('/settings')
    def settings():
        parameters = {}
        parameters['active_page'] = 'settings'
        parameters['title'] = 'Settings'
        return render_template('settings.html', **parameters)

    @main_bp.route('/explorer')
    def explorer():
        parameters = {}
        parameters['active_page'] = 'explorer'
        parameters['title'] = 'Explorer'
        return render_template('explorer.html', **parameters)

    @main_bp.route('/how_to_configure')
    def how_to_configure():
        parameters = {}
        parameters['active_page'] = 'how_to_configure'
        parameters['title'] = 'How to configure'
        return render_template('how_to_configure.html', **parameters)

    @main_bp.route('/element/create', methods=['GET', 'POST'])
    def element_create():
        form = server.forms['element']()
        if form.validate_on_submit():
            print(form.category.data)
            print(server.config['database']['categories'][int(form.category.data) - 1])
            new_element = server.categories[server.config['database']['categories'][int(form.category.data) - 1]](
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

    server.app.register_blueprint(main_bp)

# @main_bp.route('/element/copy', methods=['GET', 'POST'])
# def element_copy():
#     parameters = {}
#     parameters['active_page'] = 'copy_element'
#     parameters['title'] = 'Copy element'
#     return render_template('element_form.html', **parameters)

# @main_bp.route('/element/edit', methods=['GET', 'POST'])
# def element_edit():
#     parameters = {}
#     parameters['active_page'] = 'edit_element'
#     parameters['title'] = 'Edit element'
#     return render_template('element_form.html', **parameters)


from pathlib import Path
from app.utils import files
from flask_socketio import SocketIO, send, emit

def socketioRoutes(server):
    @server.socketio.on('explorer-get-files')
    def handle_message(msg):
        result = files.listFilesWithType(Path('.cache') / msg['path'])
        for i in result:
            if i[0].startswith('.'):
                result.remove(i)
        emit('explorer-files', result)