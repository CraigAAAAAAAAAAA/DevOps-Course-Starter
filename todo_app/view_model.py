from flask_login import current_user
import os

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def is_writer(self):
        return os.getenv('LOGIN_DISABLED') == 'True' or 'writer' in current_user.roles
    
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
    def in_progress(self):
        items_in_progress = []
        for mark_in_progress in self.items:
            if mark_in_progress.status == "Started":
                items_in_progress.append(mark_in_progress)        
        return items_in_progress

    @property
    def done_items(self):
        items_done = []
        for mark_done in self.items:
            if mark_done.status == "Done":
                items_done.append(mark_done)        
        return items_done