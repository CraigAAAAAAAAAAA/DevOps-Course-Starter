import functools
from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.view_model import ViewModel
from todo_app.todomongo import add_todo_item, items, update_status, delete_item
import requests
import os
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from loggly.handlers import HTTPSHandler
from logging import Formatter

class User (UserMixin):
    def __init__(self, id):
        self.id = id
        self.is_reader = True
        if id == '97612224':
            self.roles=['reader', 'writer']
        else:
            self.roles=['reader']

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'
    app.logger.setLevel(os.getenv('LOG_LEVEL'))
    
    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(
            f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
    handler.setFormatter(
        Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )
    app.logger.addHandler(handler)

    login_manager = LoginManager()
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        redirect_url= f"https://github.com/login/oauth/authorize?client_id={os.getenv('GITHUB_CLIENT_ID')}"

        app.logger.info("New user attempted to use the app")

        return redirect(redirect_url)
    
   
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    
    login_manager.init_app(app)


    def writer_required(func):
        @functools.wraps(func)
        def forbidden_if_not_writer_func(*args, **kwargs):
            if os.getenv('LOGIN_DISABLED') == 'True' or 'writer' in current_user.roles:
                return func(*args, **kwargs)
            else:
                app.logger.warning("Unauthorised user")
                return "Forbidden", 403

        return forbidden_if_not_writer_func

    
    @app.route('/')
    @login_required
    def index():

        item_view_model = ViewModel(items())
        return render_template('index.html', view_model=item_view_model)
    
    @app.route('/callback')
    def callback():
        auth_code = request.args.get('code')
        access_token_url = 'https://github.com/login/oauth/access_token'

        payload = {
            "client_id": os.getenv('GITHUB_CLIENT_ID'),
            "client_secret": os.getenv('GITHUB_CLIENT_SECRET'),
            "code": auth_code,
            }

        headers = {
            "Accept": "application/json"
        }

        response = requests.post(access_token_url, data = payload, headers = headers)

        access_token = response.json()['access_token']

        user_info_url = 'https://api.github.com/user'

        auth_header = {
            "Authorization": f"Bearer {access_token}"
        }

        user_info_response = requests.get(user_info_url, headers= auth_header)

        user_id = user_info_response.json()['id']

        user = User(str(user_id))

        login_user(user)

        app.logger.info("User Logged in: %s", user_id)

        return redirect('/')

    @app.route('/add_task', methods=['POST'])
    @login_required
    @writer_required
    def add_new_item():
        try:
            title = request.form['todo_title']
            add_todo_item(title)

            app.logger.info("New task added: %s", title)

        except add_new_item as e:
            app.logger.error("New task error: %s", title, exc_info=True)
               
        return redirect ('/')

    @app.route('/progress', methods=['POST'])
    @login_required
    @writer_required
    def in_progress():
        try:
            item_id = request.form['item_id']
            update_status(item_id, 'started')
            
            app.logger.info("Task Started: %s", item_id)
        
        except in_progress as e:
            app.logger.error("Task status did not update: %s", item_id, exc_info=True)
  
        return redirect ('/')
        
    @app.route('/mark_done', methods=['POST'])
    @login_required
    @writer_required
    def mark_done():
        try:
            item_id = request.form['item_id']
            delete_item(item_id)
            
            app.logger.info("Task Finished: %s", item_id)
        
        except mark_done as e:
            app.logger.error("Task was not completed: %s", item_id, exc_info=True)
        
        return index ()

    return app

    















