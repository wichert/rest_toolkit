from rest_toolkit import resource


@resource('/')
class RootResource(object):
    def __init__(self, request):
        pass


@RootResource.controller('engage')
def root_engage(resource, request):
    return {'message': 'Ai ai captain'}


@RootResource.controller('engage', request_method='GET')
def get_engage(resource, request):
    return {'message': 'Warp engine offline'}


@resource('/resource')
class Resource(object):
    def __init__(self, request):
        pass


@Resource.controller('engage')
def engage(resource, request):
    return {'message': 'Ai ai captain'}
