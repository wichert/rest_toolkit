class RestState(object):
    def __init__(self, resource_class, route_path, route_name=None):
        self.resource_class = resource_class
        self.route_path = route_path
        self.views = {}
        self.controllers = {}
        if route_name:
            self.route_name = route_name
        else:
            self.route_name = 'rest-%s' % self.resource_class.__name__

    def add_method(self, method, view):
        self.views[method] = view

    def add_controller(self, name, view, method):
        self.controllers[(name, method)] = view

    @classmethod
    def add_to_resource(cls, resource_class, route_path, route_name):
        resource_class.__rest__ = state = RestState(resource_class,
                route_path, route_name)
        return state

    @classmethod
    def from_resource(cls, resource_class):
        return resource_class.__rest__

    def supported_methods(self):
        return set(self.views) | {'OPTIONS'}
