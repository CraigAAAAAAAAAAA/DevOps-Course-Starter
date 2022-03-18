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
    def mark_done(self):
        items_done = []
        for mark_done in self.items:
            if mark_done.status == "Done":
                items_done.append(mark_done)        
        return items_done