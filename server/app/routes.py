from flask import Blueprint, render_template, redirect, url_for, jsonify
import app.utils.forms as forms
from app.utils.database import count_todays_entries, last_entry
from pathlib import Path
from app.utils import files
from datetime import datetime, timedelta
from flask_socketio import emit
from flask import send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.exceptions import HTTPException
import os
from flask import send_from_directory

def condition_decorator(decorator, condition):
    def wrapper(func):
        return decorator(func) if condition else func
    return wrapper

def set_routes(server):
    
    @server.app.route('/datasheets/<category>/<id>')
    def show_datasheet(category, id):
        subfolder = os.path.join(server.app.config["UPLOAD_FOLDER"], category)
        os.makedirs(subfolder, exist_ok=True)
        return send_from_directory(subfolder, id + '.pdf', mimetype='application/pdf', as_attachment = False)
    
    @server.app.route('/')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def index():
        return redirect(url_for('dashboard'))

    @server.app.route('/dashboard')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def dashboard():
        parameters = {}
        parameters['active_page'] = 'dashboard'
        parameters['title'] = 'Dashboard'
        parameters['footprints_amount'] = server.filling_site_data["symbols_amount"]
        parameters['symbols_amount'] = server.filling_site_data["footprints_amount"]
        parameters['elemenents_amount'] = sum([server.models.categories[i].query.count() for i in server.models.categories])
        parameters['elements_todays_amount'] = sum([count_todays_entries(server.models.categories[i]) for i in server.models.categories])
        parameters['last_element_added'] = last_entry(list(server.models.categories.values())).part_name
        parameters['are_users_enabled'] = server.config['database']['users']['is_enabled']
        parameters['categories_elements_amount'] = {key:server.models.categories[key].query.count() for key in server.models.categories}
        return render_template('dashboard.html', **parameters)

    @server.app.route('/search_components')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def search_compontents():
        parameters = {}
        parameters['active_page'] = 'search_components'
        parameters['title'] = 'Search components'
        # parameters['components'] = [x for i in server.models.categories for x in server.models.categories[i].query.all()]
        return render_template('search_components.html', **parameters)

    @server.app.route('/settings')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def settings():
        parameters = {}
        parameters['active_page'] = 'settings'
        parameters['title'] = 'Settings'
        parameters['are_users_enabled'] = server.config['database']['users']['is_enabled']

        change_user_data_form = None
        add_user_form = None

        if parameters['are_users_enabled']:

            change_user_data_form = server.forms['change_user_data']()
            if change_user_data_form.validate_on_submit():
                pass
            parameters['change_user_data_form'] = change_user_data_form

            add_user_form = server.forms['add_user']()
            if add_user_form.validate_on_submit():
                pass
            parameters['add_user_form'] = add_user_form

        return render_template('settings.html', **parameters) 
        
    @server.app.route('/explorer')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def explorer():
        parameters = {}
        parameters['active_page'] = 'explorer'
        parameters['title'] = 'Explorer'
        return render_template('explorer.html', **parameters)

    @server.app.route('/how_to_configure')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def how_to_configure():
        parameters = {}
        parameters['active_page'] = 'how_to_configure'
        parameters['title'] = 'How to configure'
        return render_template('how_to_configure.html', **parameters)
    
    @server.app.route('/error/<int:code>')
    def error(code):
        return render_template("error.html", code=code), code

    @server.app.errorhandler(HTTPException)
    def handle_http_error(e):
        return redirect(url_for('error', code = e.code))

    def generate_description(form):
        if not server.config['database']['elements']['is_llm_description_generation_enabled']:
            return {"mode": "description", 'status': False, "content": "None"}
        else:
            return {"mode": "description", 'status': True, "content": "Generated description for " + form.part_name.data + "."}

    def create_element(form):
        try:
            category = server.config['database']['elements']['categories_tables_name'][int(form.category.data) - 1]
            new_element = server.models.categories[category](
                part_name = form.part_name.data,
                manufacturer = form.manufacturer.data,
                manufacturer_part_name = form.manufacturer_part_name.data,
                value = form.value.data,
                availability = form.availability.data,
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
            if form.datasheet.data != "":
                subfolder = os.path.join("datasheets", category)
                os.makedirs(subfolder, exist_ok=True)
                filename = new_element.uuid + ".pdf"
                filepath = os.path.join(subfolder, filename)
                form.datasheet.data.save(filepath)
            else:
                pass
            server.db.session.commit()
            return {"uuid":new_element.uuid, "category":category}
        except:
            return None

    @server.app.route('/element/create', methods=['GET', 'POST'])
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def element_create():
        form = server.forms['creating_element']()

        if form.validate_on_submit():
            if form.generate_description.data:
                result = generate_description(form)
                result = jsonify(result)
            else:
                result = create_element(form)
                print(result)
                if result != None:
                    return redirect(url_for("element_details", category=result["category"], id=result["uuid"]))
                else:
                    return redirect(url_for('error', code = 400))
            return result
        parameters = {}
        parameters['active_page'] = 'create_element'
        parameters['title'] = 'Create element'
        parameters['form'] = form
        return render_template('element_form.html', **parameters)
    
    @server.app.route('/element/details/<category>/<string:id>')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def element_details(category, id):
        if category in server.models.categories.keys():
            element = server.models.categories[category].query.filter_by(uuid=id).first()
            if element != None:
                parameters = {}
                parameters["uuid"] = id
                parameters['part_name'] = element.part_name
                parameters['manufacturer'] = element.manufacturer
                parameters['manufacturer_part_name'] = element.manufacturer_part_name
                parameters['category'] = category
                parameters['description'] = element.description
                parameters['value'] = category
                parameters['availability'] = element.availability
                parameters['library_ref'] = element.library_ref
                parameters['library_path'] = element.library_path
                parameters['footprint_ref_1'] = element.footprint_ref_1
                parameters['footprint_path_1'] = element.footprint_path_1
                parameters['footprint_ref_2'] = element.footprint_ref_2
                parameters['footprint_path_2'] = element.footprint_path_2
                parameters['footprint_ref_3'] = element.footprint_ref_3
                parameters['footprint_path_3'] = element.footprint_path_3
                return render_template('element_details.html', **parameters)
        return redirect(url_for('error', code = 400))
        

        


    def element_edit():
        pass

    def element_copy():
        pass

    def element_delete():
        pass

    if server.config['database']['users']['is_enabled']:
        
        @server.login_manager.user_loader
        def load_user(user_id):
            try:
                return server.models.user.query.get(int(user_id))
            except Exception:
                return None
        
        def find_user(username):
            user = server.models.user.query.filter_by(username = username).first()
            if user == None:
                user = server.models.user.query.filter_by(email = username).first()
            return user

        @server.app.route("/login", methods=["GET", "POST"])
        def login():
            form = server.forms['login']()
            if form.validate_on_submit():
                user = find_user(form.username.data)
                print(server.bcrypt.generate_password_hash(form.password.data).decode("utf-8"))
                if user and server.bcrypt.check_password_hash(user.password, form.password.data):
                    # # sprawdź datę wygaśnięcia
                    # if user.expired_access_time and user.access_expires < datetime.utcnow():
                    #     print("Dostęp wygasł dla tego konta.", "warning")
                    #     return redirect(url_for("login"))
                    login_user(user)
                    print("Zalogowano pomyślnie.", "success")
                    next_page = request.args.get("next")
                    return redirect(next_page or url_for("dashboard"))
                print("Błędny login lub hasło.", "danger")
            return render_template("login.html", form=form)
        
        @server.app.route("/logout")
        @login_required
        def logout():
            logout_user()
            return redirect(url_for("login"))
        

def set_socketio_routes(server):

    @server.socketio.on('explorer-get-files')
    def explorer_get_files(msg):
        result = files.list_files_with_type(Path('.cache') / msg['path'])
        for i in result:
            if i[0].startswith('.'):
                result.remove(i)
        emit('explorer-files', result)