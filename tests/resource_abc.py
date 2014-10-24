from rest_toolkit import resource
from rest_toolkit.abc import ViewableResource
from pyramid.security import Allow
from pyramid.security import Authenticated


@resource('/')
class Resource(ViewableResource):
    def __init__(self, request):
        pass

    def to_dict(self):
        return {'message': 'Hello, world'}


@resource('/secure', read_permission='view')
class SecureResource(ViewableResource):
    __acl__ = [(Allow, Authenticated, ['view'])]

    def __init__(self, request):
        pass

    def to_dict(self):
        return {'message': 'Hello, world'}
