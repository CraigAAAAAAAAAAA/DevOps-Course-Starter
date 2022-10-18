from flask import Flask, render_template, request, redirect
from todo_app.todo import Item
from todo_app.flask_config import Config
from todo_app.view_model import ViewModel
from todo_app.todomongo import add_todo_item, items, update_status, delete_item

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())


    @app.route('/')

    def index():

        item_view_model = ViewModel(items())
        return render_template('index.html',
        view_model=item_view_model)

    @app.route('/add_task', methods=['POST'])
    def add_new_item():

        title = request.form['todo_title']
        add_todo_item(title)
        
        return redirect ('/')

    @app.route('/progress', methods=['POST'])
    def in_progress():

        item_id = request.form['item_id']
        update_status(item_id, 'in progress')
  
        return redirect ('/')
        
    @app.route('/mark_done', methods=['POST'])
    def mark_done():

        item_id = request.form['item_id']
        delete_item(item_id)
        
        return index ()

    return app

    















