import os
import pytest
from threading import Thread
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
from todo_app import app
from todo_app.todo import Item
import pymongo

@pytest.fixture(scope='module')
def app_with_temp_db():
    # Load our real environment variables
    load_dotenv(override=True)
    os.environ['LOGIN_DISABLED'] = 'True'

    # Create the new board & update the board id environment variable
    
    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['test_items']

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
    delete_testdb()

def items():

    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['test_items']

    mongo_items = collection.find()

    return [Item.from_mongo_item(mongo_item) for mongo_item in mongo_items]

def delete_testdb():
    
    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['test_items']
    
    collection.drop()

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.headless = True
    with webdriver.Firefox(options=opts) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_db):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'