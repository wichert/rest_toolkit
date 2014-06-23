from rest_toolkit import resource
from pyramid.view import view_config
from .models import DemoSite


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
    return {"todos": [
        {"id": "t1", "title": "Firstie"},
        {"id": "t2", "title": "Second"},
        {"id": "t3", "title": "Another"},
        {"id": "t4", "title": "Last"}
    ]}