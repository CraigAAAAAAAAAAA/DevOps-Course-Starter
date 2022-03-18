from todo_app.todo import Item
from todo_app.view_model import ViewModel

def test_todo_items():
    items = [Item(8899, "Stuff to do", "To Do")]
    VM = ViewModel(items)
    ToDoItems = VM.todo_items
    assert len (ToDoItems) == 1