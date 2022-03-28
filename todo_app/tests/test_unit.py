from todo_app.todo import Item
from todo_app.view_model import ViewModel

def test_todo_items():
    items_to_do = [Item(2344,"Answer emails", "To do"), Item(2345,"Do exercise", "In Progress") , Item(2346,"Go Home", "Done")]
    view_model = ViewModel(items_to_do)
    to_do_items = view_model.todo_items
    assert len (to_do_items) == 1
    assert to_do_items[0].name == "Answer emails"

def test_done_items():
    items_done = [Item(2344,"Answer emails", "To do"), Item(2345,"Do exercise", "In Progress") , Item(2346,"Go Home", "Done")]
    view_model = ViewModel(items_done)
    done_items = view_model.done_items
    assert len (done_items) == 1
    assert done_items[0].name == "Go Home"

def test_in_progress():
    all_items = [Item(2344,"Answer emails", "To do"), Item(2345,"Do exercise", "In Progress") , Item(2346,"Go Home", "Done")]
    view_model = ViewModel(all_items)
    in_progress = view_model.in_progress
    assert len (in_progress) == 1
    assert in_progress[0].name == "Do exercise"