from rest_toolkit import resource
from pyramid.httpexceptions import HTTPNotFound


@resource(route_path='/keyerror')
class KeyErrorResource(object):
    def __init__(self, request):
        raise KeyError('BOOM!')


@resource(route_path='/http-error')
class HTTPErrorResource(object):
    def __init__(self, request):
        raise HTTPNotFound('BOOM!')
