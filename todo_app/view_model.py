class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        for TRELLO_LIST_TODO in self._items:
            if TRELLO_LIST_TODO
                return []

    @property
    def in_progress_items(self):
        return []

    @property
    def done_items(self):
        return []