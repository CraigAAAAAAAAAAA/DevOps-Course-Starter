from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_items, add_item

from todo_app.flask_config import Config
import requests
import os

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
     
    url = "https://api.trello.com/1/boards/vwBBuYdA/lists"

    print(os.getenv("TRELLO_API_KEY"))

    querystring = {
            "key":os.getenv("TRELLO_API_KEY"),
            "token":os.getenv("TRELLO_API_TOKEN"),
            "cards": "open"
}

    response = requests.request("GET", url, params=querystring)

    response_json = response.json()

    items = []

    for trello_list in response_json:
        for card in trello_list['cards']:
            card['status'] = trello_list['name']
            items.append(card)

    return render_template('index.html', items = items)

@app.route('/add_card', methods=['POST'])
def add_new_card(list_id, card_name):

    url = "https://api.trello.com/1/cards"

    response = requests.request("POST", url, params=querystring)

    card_id = response.json()

    title = request.form['name']

    ["id"]
    
    return index()
    






    















