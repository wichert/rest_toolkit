from random import randint

from rest_toolkit import quick_serve
from rest_toolkit import resource

todos = {
    "td1": {"id": "td1", "title": "Firstie"},
    "td2": {"id": "td2", "title": "Second"},
    "td3": {"id": "td3", "title": "Another"},
    "td4": {"id": "td4", "title": "Last"}
}


@resource('/todos')
class TodoCollection(object):
    def __init__(self, request):
        pass


@TodoCollection.GET()
def list_todos(collection, request):
    return {"todos": list(todos.values())}

@TodoCollection.POST()
def add_todo(collection, request):
    todo = {
        "id": "td" + str(randint(100, 9999)),
        "title": request.json_body["title"]
    }
    todos[todo["id"]] = todo
    return {"todo": todo}


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
    return {}

@TodoResource.DELETE()
def delete_todo(todo, request):
    del todos[todo.data["id"]]
    return {}


if __name__ == '__main__':
    quick_serve(port=8088)