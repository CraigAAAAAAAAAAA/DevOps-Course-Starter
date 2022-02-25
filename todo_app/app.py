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
def add_new_card():

    url = "https://api.trello.com/1/cards"

    title = request.form['todo_title']

    querystring = {
    "key":os.getenv("TRELLO_API_KEY"),
    "token":os.getenv("TRELLO_API_TOKEN"),
    "idList" : "620540bb9814898a4ec14f53",
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
    "idList" : "620540d8d9ab6c510fac951c",

 }

    response = requests.request("PUT", url, params=querystring)

    card_id = response.json()

    
    return index ()






    















