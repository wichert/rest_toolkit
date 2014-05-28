class RestState(object):
    def __init__(self, resource_class):
        self.resource_class = resource_class
        self.views = {}

    def route_name(self):
        return 'rest-%s' % self.resource_class.__name__

    def add_method(self, method, view):
        self.views[method] = view

    @classmethod
    def add_to_resource(cls, resource_class):
        resource_class.__rest__ = state = RestState(resource_class)
        return state

    @classmethod
    def from_resource(cls, resource_class):
        return resource_class.__rest__

    def supported_methods(self):
        return set(self.views) | {'OPTIONS'}
