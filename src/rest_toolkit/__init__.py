import venusian
from .state import RestState
from .views import unsupported_method_view
from .views import default_options_view


class resource(object):
    def __init__(self, route_path, **settings):
        self.route_path = route_path

    def callback(self, scanner, name, cls):
        config = scanner.config.with_package(self.module)
        route_name = 'rest-%s' % cls.__name__
        config.add_route(route_name, self.route_path, factory=cls)
        config.add_view(default_options_view, route_name=route_name,
                request_method='OPTIONS')
        config.add_view(unsupported_method_view, route_name=route_name)

    def __call__(self, cls):
        RestState.add_to_resource(cls)
        info = venusian.attach(cls, self.callback, 'pyramid')
        self.module = info.module
        return cls
