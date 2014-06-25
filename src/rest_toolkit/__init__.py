from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.path import caller_package
from pyramid.path import package_path
import venusian
from .state import RestState
from .views import unsupported_method_view
from .views import default_options_view


METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']


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


class ControllerDecorator(BaseDecorator):
    default_arguments = {'renderer': 'json'}

    def __init__(self, name, **kw):
        self.name = name
        self.view_arguments = self.default_arguments.copy()
        self.view_arguments.update(kw)

    def callback(self, scanner, name, view):
        config = scanner.config.with_package(self.module)
        route_path = ''.join([self.state.route_path,
                              '' if self.state.route_path.endswith('/') else '',
                              self.name])
        route_name = '%s-%s' % (self.state.route_name(), self.name)
        self.state.add_controller(self.name, view)
        config.add_route(route_name, route_path, factory=self.state.resource_class)
        config.add_view(unsupported_method_view, route_name=route_name)
        config.add_view(view,
                route_name=route_name,
                request_method='POST',
                **self.view_arguments)


class resource(BaseDecorator):
    def __init__(self, route_path, **settings):
        self.route_path = route_path

    def callback(self, scanner, name, cls):
        state = RestState.from_resource(cls)
        config = scanner.config.with_package(self.module)
        route_name = state.route_name()
        config.add_route(route_name, state.route_path, factory=cls)
        config.add_view(default_options_view, route_name=route_name,
                request_method='OPTIONS')
        config.add_view(unsupported_method_view, route_name=route_name)

    def __call__(self, cls):
        state = RestState.add_to_resource(cls, self.route_path)
        for method in METHODS:
            setattr(cls, method, type('ViewDecorator%s' % method,
                                      (ViewDecorator, object),
                                      {'request_method': method,
                                       'state': state}))
        cls.controller = type('ControllerDecorator',
                              (ControllerDecorator, object),
                              {'state': state})
        return super(resource, self).__call__(cls, depth=2)


def includeme(config):
    config.add_view('rest_toolkit.error.generic', context=Exception, renderer='json')
    config.add_notfound_view('rest_toolkit.error.notfound', renderer='json')
    config.add_forbidden_view('rest_toolkit.error.forbidden', renderer='json')


def quick_serve(sql_session_factory=None, port=8080):
    """Start a HTTP server for your REST service.

    This function provides quick way to run a webserver for your REST service.
    The webserver will listen on port 8080 on all IP addresses of the local
    machine.

    If you need to configure the underlying Pyramid system, or you want to use
    a different HTTP server you will need to create the WSGI application
    yourself. Instead of using `quick_serve` you will need to do something like
    this:

    .. code-block:: python

       from pyramid.config import Configurator
       from wsgiref.simple_server import make_server

       config = Configurator()
       config.include('rest_toolkit')
       config.scan()
       app = config.make_wsgi_app()
       make_server('0.0.0.0', 8080, app).serve_forever()

    :param sql_session_factory: A factory function to return a SQLAlchemy
        session. This is generally a :ref:`scoped_session
        <sqlalchemy:sqlalchemy.orm.scoping.scoped_session>` instance, and
        commonly called ``Session`` or ``DBSession``.
    """
    config = Configurator()
    config.include('rest_toolkit')
    if sql_session_factory is not None:
        config.include('rest_toolkit.ext.sql')
        config.set_sqlalchemy_session_factory(sql_session_factory)
    # Publish the caller's path as a static asset view
    pkg = caller_package()
    config.add_static_view('static', package_path(pkg))
    config.scan(pkg)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()


__all__ = ['resource', 'quick_serve']