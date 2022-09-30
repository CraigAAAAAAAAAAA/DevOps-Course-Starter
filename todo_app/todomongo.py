import pymongo
import os
import dotenv
from bson.objectid import ObjectId
from todo_app.todo import Item

dotenv.load_dotenv(".env")

def items():

    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['items']

    tasks = []

    for mongo_item in collection.find():
        new_item = Item(mongo_item["_id"], mongo_item["Todo"], mongo_item["Status"])
        tasks.append(new_item)
        
    return tasks

def add_todo_item(item):
    new_mongo_item = {
        "Todo": item,
        "Status": "To_Do"
    }
    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['items']
    
    collection.insert_one(new_mongo_item)

def update_status(item_id, in_progress):
    
    item_selector = {'_id': ObjectId(item_id)}

    status_update = {
            "$set": {"Status": in_progress},
        }

    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['items']


    collection.update_one(item_selector, status_update) 

def delete_item(item_id):

    item_selector = {'_id': ObjectId(item_id)}
    
    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['items']
    
    collection.delete_one(item_selector)