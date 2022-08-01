import os
import pytest
from threading import Thread
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
from todo_app import app

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Load our real environment variables
    load_dotenv(override=True)

    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id

    # Construct the new application
    application = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    
    # Give the app a moment to start
    sleep(1)

    # Return the application object as the result of the fixture
    yield application

    # Tear down
    thread.join(1)
    delete_trello_board(board_id)

def create_trello_board():
    # TODO Create a new board in Trello and return the id
    url = "https://api.trello.com/1/boards"

    title = 'test_board'

    querystring = {
    "key":os.getenv("TRELLO_API_KEY"),
    "token":os.getenv("TRELLO_API_TOKEN"),
    "name" : title

    }

    response = requests.request("POST", url, params=querystring)

    board_id = response.json()['id']
    
    return board_id

def delete_trello_board(board_id):
    # TODO Delete the Trello board with id board_id

    url = f"https://api.trello.com/1/boards/{board_id}"

    querystring = {
    "key":os.getenv("TRELLO_API_KEY"),
    "token":os.getenv("TRELLO_API_TOKEN"),

    }

    response = requests.request("DELETE", url, params=querystring)

    response.raise_for_status()

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.headless = True
    with webdriver.Firefox(options=opts) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'