from random import randint

from rest_toolkit import (
    quick_serve,
    resource
)

from rest_toolkit.abc import (
    ViewableResource,
    EditableResource,
    DeletableResource
)

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
class TodoResource(EditableResource, ViewableResource, DeletableResource):
    def __init__(self, request):
        todo_id = request.matchdict['id']
        self.todo = todos.get(todo_id)
        if self.todo is None:
            raise KeyError('Unknown event id')

    def to_dict(self):
        return self.todo

    def update_from_dict(self, data, replace=True):
        self.todo.title = data.title
        return {}

    def validate(self, data, partial):
        pass

    def delete(self):
        del todos[self.todo["id"]]


if __name__ == '__main__':
    quick_serve(port=8088)