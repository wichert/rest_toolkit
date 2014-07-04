from rest_toolkit import resource
from rest_toolkit.abc import ViewableResource


@resource('/')
class Resource(ViewableResource):
    def __init__(self, request):
        pass

    def to_dict(self):
        return {'message': 'Hello, world'}


@Resource.GET()
def get(resource, request):
    return {'message': 'Welcome'}
