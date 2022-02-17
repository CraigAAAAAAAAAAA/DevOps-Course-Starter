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


    items = response_json[0]['cards']
    return render_template('index.html', items = items)

@app.route('/add_item', methods=['POST'])
def add_new_item():
    title = request.form['todo_title']
    add_item(title)
    return index()
    






    















