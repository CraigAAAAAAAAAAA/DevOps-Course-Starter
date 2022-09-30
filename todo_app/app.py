from flask import Flask, render_template, request, redirect
from todo_app.todo import Item
from todo_app.flask_config import Config
import requests
import os
from todo_app.view_model import ViewModel
from todo_app.todomongo import add_todo_item, items, update_status

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())


    @app.route('/')

    def index():

        item_view_model = ViewModel(items())
        return render_template('index.html',
        view_model=item_view_model)

    @app.route('/add_task', methods=['POST'])
    def add_new_task():

        title = request.form['todo_title']
        add_todo_item(title)
        
        return redirect ('/')

    @app.route('/in_progress', methods=['POST'])
    def in_progress():

        item_id = request.form[item_id, "In progress"]
        update_status(item_id)
  
        return index ()
        
    @app.route('/mark_done', methods=['POST'])
    def mark_done():

        card_id = request.form['card_id']
    
        url = f"https://api.trello.com/1/cards/{card_id}"

        querystring = {
        "key":os.getenv("TRELLO_API_KEY"),
        "token":os.getenv("TRELLO_API_TOKEN"),
        "idList" : os.getenv("TRELLO_LIST_DONE"),

        }

        response = requests.request("PUT", url, params=querystring)

        card_id = response.json()

        
        return index ()

    return app

    















