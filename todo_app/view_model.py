class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        items_to_do = []
        for my_item in self.items:
            if my_item.status == "To do":
                items_to_do.append(my_item)        
        return items_to_do

    @property
    def in_progress_items(self):
        return []

    @property
    def done_items(self):
        items_done = []
        for mark_done in self.items:
            if mark_done.status == "Done":
                items_done.append(mark_done)        
        return items_done