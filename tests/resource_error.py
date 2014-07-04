from rest_toolkit import resource
from pyramid.httpexceptions import HTTPNotFound


@resource('/keyerror')
class KeyErrorResource(object):
    def __init__(self, request):
        raise KeyError('BOOM!')


@resource('/http-error')
class HTTPErrorResource(object):
    def __init__(self, request):
        raise HTTPNotFound('BOOM!')
