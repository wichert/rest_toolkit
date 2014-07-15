from os.path import dirname
from os.path import realpath
from random import randint
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.events import NewRequest
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
    return {"data": list(todos.values())}


@TodoCollection.POST()
def add_todo(collection, request):
    todo = {
        "id": "td" + str(randint(100, 9999)),
        "title": request.json_body["title"]
    }
    todos[todo["id"]] = todo
    return {"data": todo}


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


def add_cors_callback(event):
    headers = "Origin, Content-Type, Accept, Authorization"
    def cors_headers(request, response):
        response.headers.update({
            # In production you would be careful with this
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": headers
        })

    event.request.add_response_callback(cors_headers)


if __name__ == '__main__':
    config = Configurator()
    config.include('rest_toolkit')
    # Publish the module's path as a static asset view
    config.add_static_view('static', dirname(realpath(__file__)))
    config.add_subscriber(add_cors_callback, NewRequest)
    config.scan(".")
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8088, app)
    server.serve_forever()
