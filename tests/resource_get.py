from rest_toolkit import resource


@resource(route_path='/')
class Resource(object):
    def __init__(self, request):
        pass


@Resource.GET()
def get(resource, request):
    return {'message': 'hello'}
