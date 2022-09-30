class Item: 
    def __init__(self, id, name, status): 
        self.id = id 
        self.name = name 
        self.status = status 

    @classmethod
    def from_mongo_item(cls, mongo_item):
        return cls(mongo_item['_id'], mongo_item['task'], mongo_item['Status'])