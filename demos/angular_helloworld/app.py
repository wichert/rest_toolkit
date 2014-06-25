from rest_toolkit import quick_serve
from rest_toolkit import resource


@resource('/todos')
class TodoCollection(object):
    def __init__(self, request):
        pass


@TodoCollection.GET()
def list_todos(collection, request):
    return {"todos": [
        {"id": "t1", "title": "Firstie"},
        {"id": "t2", "title": "Second"},
        {"id": "t3", "title": "Another"},
        {"id": "t4", "title": "Last"}
    ]}


if __name__ == '__main__':
    quick_serve(port=8088)