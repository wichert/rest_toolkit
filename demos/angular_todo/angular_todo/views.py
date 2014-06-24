from rest_toolkit import resource
from pyramid.view import view_config
from .models import DemoSite

todos = {
    "td1": {"id": "td1", "title": "Firstie"},
    "td2": {"id": "td2", "title": "Second"},
    "td3": {"id": "td3", "title": "Another"},
    "td4": {"id": "td4", "title": "Last"}
}


class DemoViews:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=DemoSite, renderer="templates/home.jinja2")
    def home_view(self):
        return {}


@resource('/todos')
class TodoCollection(object):
    def __init__(self, request):
        pass


@TodoCollection.GET()
def list_todos(collection, request):
    return {"todos": list(todos.values())}


@resource('/todos/{id}')
class TodoResource(object):
    def __init__(self, request):
        self.data = todos[request.matchdict['id']]


@TodoResource.GET()
def view_todo(todo, request):
    return todo.data

@TodoResource.PUT()
def update_todo(todo, request):
    todo.data['title'] = request.json_body['title']
    return todo.data
