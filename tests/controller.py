from rest_toolkit import resource


@resource('/')
class Resource(object):
    def __init__(self, request):
        pass


@Resource.controller('engage')
def engage(resource, request):
    return {'message': 'Ai ai captain'}


@Resource.controller('engage', method='GET')
def get_engage(resource, request):
    return {'message': 'Warp engine offline'}
