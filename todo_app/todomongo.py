import pymongo
import os
import dotenv

dotenv.load_dotenv(".env")

def get_items():
    return []

def add_item():
    new_mongo_item = {
        "Todo": add_item,
        "Status": "To_Do"
    }
    client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    database = client[os.getenv("MONGO_DATABASE_NAME")]
    collection = database['items']
    
    collection.insert_one(new_mongo_item)


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