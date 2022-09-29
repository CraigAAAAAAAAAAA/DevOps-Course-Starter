from gc import collect
import imp
from tkinter import E
from typing import ItemsView
import pymongo
import os
import dotenv
from todo_app.view_model import items, todo_items, in_progress, done_items

dotenv.load_dotenv(".env")

def items():
    return [items]

def todo_items():
    new_mongo_item = {
        "Todo": todo_items,
        "Status": "To_Do"
    }
    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['items']
    
    collection.insert_one(new_mongo_item)

def update_status(_id):
    from bson.objectid import ObjectId
    
    ObjectId = ObjectId(_id)
if todo_items in items == in_progress:

    status_update = {
        "$set": {"Status": in_progress},
    }

    items.update_one(status_update)

else:
    
    item_done = {
        "$set": {"Status": done_items}
    }
    
    items.item_done.delete_one(done_items)


# def delete_item_by_status(_id):
#     from bson.objectid import ObjectId

#     ObjectId = ObjectId(_id)

#     item_done = {
#         "$set": {"Status": done_items}
#     }
    
#     collection.item_delete.delete_one(done_items)
    
#     client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
#     database = client[os.getenv("MONGO_DATABASE_NAME")]
#     collection = database['items']

# def update_status(Status):
#     _update = {
#         "$set": {"Status": "Done"}
#     }
#     collection.update_one(_update)

# update_status(_update)
    

# db_entry = {"author": "Craig", "text": "My test"}
# collection.insert_one(db_entry)
# documents = list(collection.find())
# print(documents)