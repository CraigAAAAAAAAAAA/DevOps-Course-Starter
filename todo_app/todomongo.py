import pymongo
import os
from bson.objectid import ObjectId
from todo_app.todo import Item

def items():

    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['items']

    mongo_items = collection.find()

    return [Item.from_mongo_item(mongo_item) for mongo_item in mongo_items]

def add_todo_item(items):
    new_mongo_item = {
        "Todo": items,
        "Status": "To Do"
    }
    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['items']
    
    collection.insert_one(new_mongo_item)

def update_status(item_id, progress):
    
    item_selector = {'_id': ObjectId(item_id)}

    status_update = {
            "$set": {"Status": progress}
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