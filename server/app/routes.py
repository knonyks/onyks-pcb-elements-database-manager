from flask import Blueprint, render_template, redirect, url_for
import app.utils.forms as forms
from app.utils.database import count_todays_entries, last_entry
from pathlib import Path
from app.utils import files
from datetime import datetime, timedelta
from flask_socketio import emit
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.exceptions import HTTPException

def condition_decorator(decorator, condition):
    def wrapper(func):
        return decorator(func) if condition else func
    return wrapper

def set_routes(server):

    @server.app.route('/')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def index():
        parameters = {}
        parameters['title'] = 'Dashboard'
        return redirect(url_for('dashboard', **parameters))

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
        return render_template('dashboard.html', **parameters)

    @server.app.route('/search_components')
    @condition_decorator(login_required, server.config['database']['users']['is_enabled'])
    def search_compontents():
        parameters = {}
        parameters['active_page'] = 'search_components'
        parameters['title'] = 'Search components'
        parameters['components'] = [x for i in server.models.categories for x in server.models.categories[i].query.all()]
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
        return redirect(url_for('show_error', code=e.code))

    def generate_description(form):
        print(form.datasheet.data)

    # def createElement(form):
    #     print(form.category.data)
    #     print(server.config['database']['categories'][int(form.category.data) - 1])
    #     new_element = server.models[server.config['database']['categories'][int(form.category.data) - 1]](
    #         part_name = form.part_name.data,
    #         manufacturer = form.manufacturer.data,
    #         description = form.description.data,
    #         library_ref = form.library_ref.data,
    #         library_path = form.library_path.data,
    #         footprint_ref_1 = form.footprint_ref_1.data,
    #         footprint_path_1 = form.footprint_path_1.data,
    #         footprint_ref_2 = form.footprint_ref_2.data,
    #         footprint_path_2 = form.footprint_path_2.data,
    #         footprint_ref_3 = form.footprint_ref_3.data,
    #         footprint_path_3 = form.footprint_path_3.data
    #     )
    #     server.db.session.add(new_element)
    #     server.db.session.commit()

    # @server.app.route('/element/create', methods=['GET', 'POST'])
    # @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    # def element_create():
    #     form = server.forms['creatingElement']()
    #     if form.validate_on_submit():
    #         if form.accept.data:
    #             createElement(form)
    #         elif form.generate_description.data:
    #             generateDescription(form)
    #     parameters = {}
    #     parameters['active_page'] = 'create_element'
    #     parameters['title'] = 'Create element'
    #     parameters['form'] = form
    #     return render_template('element_form.html', **parameters)
    if server.config['database']['users']['is_enabled']:
        
        @server.loginManager.user_loader
        def load_user(user_id):
            try:
                return server.models.user.query.get(int(user_id))
            except Exception:
                return None
            
        @server.app.route("/login", methods=["GET", "POST"])
        def login():
            form = server.forms['login']()
            if form.validate_on_submit():
                user = server.models.user.query.filter_by(username=form.username.data).first()
                if user == None:
                    user = server.models.user.query.filter_by(email=form.username.data).first()
                print(datetime.utcnow())
                print(server.bcrypt.generate_password_hash(form.password.data).decode("utf-8"))
                if user and server.bcrypt.check_password_hash(user.password, form.password.data):
                    # sprawdź datę wygaśnięcia
                    if user.expired_access_time and user.access_expires < datetime.utcnow():
                        print("Dostęp wygasł dla tego konta.", "warning")
                        return redirect(url_for("login"))
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
            print("Wylogowano.", "info")
            return redirect(url_for("login"))
        


def set_socketio_routes(server):

    @server.socketio.on('explorer-get-files')
    def explorer_get_files(msg):
        result = files.list_files_with_type(Path('.cache') / msg['path'])
        for i in result:
            if i[0].startswith('.'):
                result.remove(i)
        emit('explorer-files', result)