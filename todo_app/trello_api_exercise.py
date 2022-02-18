import requests
import dotenv
import os

url = "https://api.trello.com/1/boards/vwBBuYdA/lists"

dotenv.load_dotenv(".env")

print(os.getenv("TRELLO_API_KEY"))

querystring = {
    "key":os.getenv("TRELLO_API_KEY"),
    "token":os.getenv("TRELLO_API_TOKEN"),
    "cards": "open"
 }

response = requests.request("GET", url, params=querystring)

print(response.text)

url = "https://api.trello.com/1/cards"

querystring = {
    "key":os.getenv("TRELLO_API_KEY"),
    "token":os.getenv("TRELLO_API_TOKEN"),
    "idList" : "620540bb9814898a4ec14f53",
    "name" : name

 }

response = requests.request("POST", url, params=querystring)
card_id= response.json() ["id"]


print(response.text)