import pymongo
import os
import dotenv

dotenv.load_dotenv(".env")
client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
database_names = client.list_database_names()
collection = client.TestDB.CollectionOne
db_entry = {"author": "Craig", "text": "My test"}
db_entries = db_entry
entry_id = db_entry.insert_one(collection).inserted_id
documents = list(collection.find())
print(documents)