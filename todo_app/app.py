from pickletools import long1
from flask import Flask, render_template, request, redirect
from todo_app.todo import Item
from todo_app.flask_config import Config
from todo_app.view_model import ViewModel
from todo_app.todomongo import add_todo_item, items, update_status, delete_item
import requests
import os
from flask_login import LoginManager 

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config())

    login_manager = LoginManager()
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        pass 
        
    url = f"https://github.com/login/oauth/authorize"

    querystring = {
                "client_id":os.getenv("CLIENT_ID")
        }

    response = requests.request.get(url, params=querystring)

    response_json = response.json()
# Add logic to redirect to the GitHub OAuth flow when unauthenticated
 
    @login_manager.user_loader
    def load_user(user_id):
        pass # We will return to this later
 
    login_manager.init_app(app)
    
    @app.route('/')
    @login_required()

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

    















