import venusian
from .state import RestState
from .views import unsupported_method_view
from .views import default_options_view


METHODS = ['DELETE', 'GET', 'OPTIONS', 'POST', 'PUT']


class BaseDecorator(object):
    def __call__(self, wrapped, depth=1):
        info = venusian.attach(wrapped, self.callback, 'pyramid', depth=depth)
        self.module = info.module
        return wrapped


class ViewDecorator(BaseDecorator):
    default_arguments = {'renderer': 'json'}

    def __init__(self, **kw):
        self.view_arguments = self.default_arguments.copy()
        self.view_arguments.update(kw)

    def callback(self, scanner, name, view):
        config = scanner.config.with_package(self.module)
        route_name = self.state.route_name()
        self.state.add_method(self.request_method, view)
        config.add_view(view,
                route_name=route_name,
                request_method=self.request_method,
                **self.view_arguments)


class resource(BaseDecorator):
    def __init__(self, route_path, **settings):
        self.route_path = route_path

    def callback(self, scanner, name, cls):
        state = RestState.from_resource(cls)
        config = scanner.config.with_package(self.module)
        route_name = state.route_name()
        config.add_route(route_name, self.route_path, factory=cls)
        config.add_view(default_options_view, route_name=route_name,
                request_method='OPTIONS')
        config.add_view(unsupported_method_view, route_name=route_name)

    def __call__(self, cls):
        state = RestState.add_to_resource(cls)
        for method in METHODS:
            setattr(cls, method, type('ViewDecorator%s' % method,
                                      (ViewDecorator, object),
                                      {'request_method': method,
                                       'state': state}))
        return super(resource, self).__call__(cls, depth=2)
