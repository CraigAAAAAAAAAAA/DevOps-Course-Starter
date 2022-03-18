class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        items_to_do = []
        for myItem in self.items:
            if myItem.status == "To Do":
                items_to_do.append(myItem)        
        return items_to_do

    @property
    def in_progress_items(self):
        return []

    @property
    def done_items(self):
        return []