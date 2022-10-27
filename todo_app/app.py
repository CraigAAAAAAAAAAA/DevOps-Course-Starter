from http import client
from pickletools import long1
from flask import Flask, render_template, request, redirect
from todo_app.todo import Item
from todo_app.flask_config import Config
from todo_app.view_model import ViewModel
from todo_app.todomongo import add_todo_item, items, update_status, delete_item
import requests
import os
from flask_login import LoginManager, UserMixin
from flask_login import login_required, login_user

class User (UserMixin):
    def __init__(self, id):
        self.id = id

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    login_manager = LoginManager()
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        redirect_url= f"https://github.com/login/oauth/authorize?client_id={os.getenv('GITHUB_CLIENT_ID')}"
        return redirect(redirect_url)
   
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
    
    login_manager.init_app(app)
    
    @app.route('/')
    @login_required
    def index():

        item_view_model = ViewModel(items())
        return render_template('index.html',
        view_model=item_view_model)
    
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

        pass

        user_id = user_info_response.json()['id']

        user = User(user_id)

        login_user(user)

        return redirect('/')

    @app.route('/add_task', methods=['POST'])
    @login_required
    def add_new_item():

        title = request.form['todo_title']
        add_todo_item(title)
        
        return redirect ('/')

    @app.route('/progress', methods=['POST'])
    @login_required
    def in_progress():

        item_id = request.form['item_id']
        update_status(item_id, 'in progress')
  
        return redirect ('/')
        
    @app.route('/mark_done', methods=['POST'])
    @login_required
    def mark_done():

        item_id = request.form['item_id']
        delete_item(item_id)
        
        return index ()

    return app

    















