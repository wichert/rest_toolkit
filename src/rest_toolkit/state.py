class RestState(object):
    def __init__(self, resource):
        self.resource = resource
        self.views = {}

    def add_method(self, method, view):
        if method in self.views:
            raise ValueError('Multiple %s views for resource %s',
                    method, self.resource)
        self.views[method] = view

    @classmethod
    def add_to_resource(cls, resource):
        resource.__rest__ = RestState(resource)

    @classmethod
    def from_resource(cls, resource):
        return resource.__rest__

    def supported_methods(self):
        return set(self.views) | {'OPTIONS'}
