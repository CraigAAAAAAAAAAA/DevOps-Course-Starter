class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        for myItem in self.items:
            if item.list == "To Do":
                todo_items.append(myItem)        
        return items

    @property
    def in_progress_items(self):
        return []

    @property
    def done_items(self):
        return []