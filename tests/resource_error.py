from rest_toolkit import resource
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPPaymentRequired
from pyramid.httpexceptions import HTTPBadRequest


@resource('/keyerror')
class KeyErrorResource(object):
    def __init__(self, request):
        raise KeyError('BOOM!')


@resource('/http-error')
class HTTPErrorResource(object):
    def __init__(self, request):
        raise HTTPPaymentRequired('BOOM!')


@resource('/http-not-found')
class HTTPNotFoundResource(object):
    def __init__(self, request):
        raise HTTPNotFound()


@resource('/http-found')
class HTTPFoundResource(object):
    def __init__(self, request):
        raise HTTPFound('http://www.wiggy.net')


@resource('/custom-json-exception')
class CustomException(object):
    def __init__(self, request):
        raise HTTPBadRequest(json={'foo': 'bar'})
