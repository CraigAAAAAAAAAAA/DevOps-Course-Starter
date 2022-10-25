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
from flask_login import login_required

class User (UserMixin):
    def __init__(self, id):
        self.id = id

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config())

    login_manager = LoginManager()
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect ('https://github.com/login/oauth/authorize?client_id=51479667196a085f5024')
# Add logic to redirect to the GitHub OAuth flow when unauthenticated
    
    @app.route('/login/callback/<code>', methods=['GET'])
    def callback():
        code = request.args.get('code')
        
        url = 'https://github.com/login/oauth/access_token'

        payload = {
            "client_id": os.getenv('CLIENT_ID'),
            "client_secret": os.getenv('CLIENT_SECRET'),
            "code": code,
            "redirect_url": 'http//localhost:5000'
        }

        headers = {
            "Accept": "application/json"
        }

        requests.request("POST", url, data = payload, headers = headers)
    
    @app.route('/login/oauth/<access_token>', methods=['GET'])
    def response():
        access_token = request.args.get('access_token')

        Accept: application/json
        {
        "access_token": access_token,
        "scope":"repo,gist",
        "token_type":"bearer"
        }

        response = requests.request("POST", params=Accept)

        Accept= response.json()

    
    @login_manager.user_loader
    def load_user(user_id):
        pass # We will return to this later
 
    login_manager.init_app(app)
    
    @app.route('/')
    @login_required

    def index():

        item_view_model = ViewModel(items())
        return render_template('index.html',
        view_model=item_view_model)

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

    















