from rest_toolkit import resource


@resource('/users/{id}', route_name='user')
class Resource(object):
    def __init__(self, request):
        pass
