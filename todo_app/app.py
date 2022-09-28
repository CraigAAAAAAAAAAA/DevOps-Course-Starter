from flask import Flask, render_template, request, redirect
from todo_app.todo import Item
import todo_app.data.session_items as mongo_item

from todo_app.flask_config import Config
import requests
import os
from todo_app.view_model import ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())


    @app.route('/')
    def index():
        
        url = f"https://api.trello.com/1/boards/{os.getenv('TRELLO_BOARD_ID')}/lists"

        querystring = {
                "key":os.getenv("TRELLO_API_KEY"),
                "token":os.getenv("TRELLO_API_TOKEN"),
                "cards": "open"
        }

        response = requests.get(url, params=querystring)

        response_json = response.json()

        items = []

        for trello_list in response_json:
            for card in trello_list['cards']:
                myItem = Item(card['id'] , card['name'] , trello_list['name'])
                items.append(myItem)

        item_view_model = ViewModel(items)
        return render_template('index.html',
        view_model=item_view_model)

    @app.route('/add_card', methods=['POST'])
    def add_new_card():

        url = "https://api.trello.com/1/cards"

        title = request.form['todo_title']

        querystring = {
        "key":os.getenv("TRELLO_API_KEY"),
        "token":os.getenv("TRELLO_API_TOKEN"),
        "idList" : os.getenv("TRELLO_LIST_TODO"),
        "name" : title

        }

        response = requests.request("POST", url, params=querystring)

        card_id = response.json()
        
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

    @app.route('/in_progress', methods=['POST'])
    def in_progress():

        card_id = request.form['card_id']
    
        url = f"https://api.trello.com/1/cards/{card_id}"

        querystring = {
        "key":os.getenv("TRELLO_API_KEY"),
        "token":os.getenv("TRELLO_API_TOKEN"),
        "idList" : os.getenv("TRELLO_LIST_IN_PROGRESS"),

        }

        response = requests.request("PUT", url, params=querystring)

        card_id = response.json()

        
        return index ()

    return app

    















