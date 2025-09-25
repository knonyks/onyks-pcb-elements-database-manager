from flask import Blueprint, render_template, redirect, url_for
import app.utils.forms as forms
from app.utils.database import countTodaysEntries
from pathlib import Path
from app.utils import files
from datetime import datetime, timedelta
from flask_socketio import emit
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, redirect, url_for, flash, request


def conditionDecorator(decorator, condition):
    def wrapper(func):
        return decorator(func) if condition else func
    return wrapper

def setRoutes(server):

    @server.app.route('/')
    @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    def index():
        parameters = {}
        parameters['title'] = 'Dashboard'
        return redirect(url_for('dashboard', **parameters))

    @server.app.route('/dashboard')
    @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    def dashboard():
        parameters = {}
        parameters['active_page'] = 'dashboard'
        parameters['title'] = 'Dashboard'
        parameters['componentsDatabaseCount'] = sum([server.models[i].query.count() for i in server.config['database']['categories']])
        parameters['componentsDatabaseTodaysCount'] = sum([countTodaysEntries(server.db, server.models[i], 'Europe/Warsaw') for i in server.config['database']['categories']])
        # parameters['componentsDatabaseLastAddedPartName'] = models.Components.query.order_by(models.Components.created_at.desc()).first().part_name
        parameters['componentsFootprintsCount'] = server.siteDataFill['footprintsAmount']
        parameters['componentsSymbolsCount'] = server.siteDataFill['symbolsAmount']
        parameters['usersEnabled'] = server.config['database']['usersEnabled']
        return render_template('dashboard.html', **parameters)

    @server.app.route('/search_components')
    @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    def search_compontents():
        parameters = {}
        parameters['active_page'] = 'search_components'
        parameters['title'] = 'Search components'
        parameters['components'] = server.models['Resistors'].query.all()
        return render_template('search_components.html', **parameters)

    @server.app.route('/settings')
    @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    def settings():
        parameters = {}
        parameters['active_page'] = 'settings'
        parameters['title'] = 'Settings'
        parameters['usersEnabled'] = server.config['database']['usersEnabled']
        changeUserDataForm = None
        addUserForm = None
        if parameters['usersEnabled']:
            changeUserDataForm = server.forms['changeUserDataForm']()
            if changeUserDataForm.validate_on_submit():
                pass
            parameters['changeUserDataForm'] = changeUserDataForm

            addUserForm = server.forms['addUserForm']()
            if addUserForm.validate_on_submit():
                pass
            parameters['addUserForm'] = addUserForm


        return render_template('settings.html', **parameters) 
        
    @server.app.route('/explorer')
    @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    def explorer():
        parameters = {}
        parameters['active_page'] = 'explorer'
        parameters['title'] = 'Explorer'
        return render_template('explorer.html', **parameters)

    @server.app.route('/how_to_configure')
    @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    def how_to_configure():
        parameters = {}
        parameters['active_page'] = 'how_to_configure'
        parameters['title'] = 'How to configure'
        return render_template('how_to_configure.html', **parameters)
    
    @server.app.route('/error')
    @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    def error():
        parameters = {}
        parameters['active_page'] = 'error'
        parameters['title'] = 'error'
        return render_template('error.html', **parameters)

    def generateDescription(form):
        print(form.datasheet.data)

    def createElement(form):
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

    @server.app.route('/element/create', methods=['GET', 'POST'])
    @conditionDecorator(login_required, server.config['database']['usersEnabled'])
    def element_create():
        form = server.forms['creatingElement']()
        if form.validate_on_submit():
            if form.accept.data:
                createElement(form)
            elif form.generate_description.data:
                generateDescription(form)
        parameters = {}
        parameters['active_page'] = 'create_element'
        parameters['title'] = 'Create element'
        parameters['form'] = form
        return render_template('element_form.html', **parameters)
    if server.config['database']['usersEnabled']:
        
        @server.loginManager.user_loader
        def load_user(user_id):
            try:
                return server.models['User'].query.get(int(user_id))
            except Exception:
                return None
            
        @server.app.route("/login", methods=["GET", "POST"])
        def login():
            form = server.forms['loginForm']()
            if form.validate_on_submit():
                user = server.models['User'].query.filter_by(username=form.username.data).first()
                if user == None:
                    user = server.models['User'].query.filter_by(email=form.username.data).first()
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
        
    @server.app.errorhandler(Exception)
    def error(e):
        return render_template('error.html', error=e.code)

def setSocketioRoutes(server):

    @server.socketio.on('explorer-get-files')
    def explorerGetFiles(msg):
        result = files.listFilesWithType(Path('.cache') / msg['path'])
        for i in result:
            if i[0].startswith('.'):
                result.remove(i)
        emit('explorer-files', result)