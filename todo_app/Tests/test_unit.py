from todo_app.todo import Item
from todo_app.view_model import ViewModel

def test_todo_items():
    items_to_do = [Item(2344,"Answer emails", "To Do"), Item(2345,"Do exercise", "In Progress") , Item(2346,"Go Home", "Done")]
    VM = ViewModel(items_to_do)
    ToDoItems = VM.todo_items
    assert len (ToDoItems) == 1
    assert ToDoItems[0].name == "Answer emails"

def test_done_items():
    items_done = [Item(2344,"Answer emails", "To Do"), Item(2345,"Do exercise", "In Progress") , Item(2346,"Go Home", "Done")]
    VM = ViewModel(items_done)
    DoneItems = VM.done_items
    assert len (DoneIems) == 1
    assert DoneItems[0].name == "Go Home"