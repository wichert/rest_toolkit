from wsgiref.simple_server import make_server
from webob.exc import WSGIHTTPException
from pyramid.config import Configurator
from pyramid.interfaces import IExceptionResponse
from pyramid.path import caller_package
from pyramid.path import package_path
import venusian
from .abc import DeletableResource
from .abc import EditableResource
from .abc import ViewableResource
from .state import RestState
from .views import unsupported_method_view
from .views import default_delete_view
from .views import default_get_view
from .views import default_options_view
from .views import default_patch_view
from .views import default_put_view


METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']


class BaseDecorator(object):
    def __call__(self, wrapped, depth=1):
        info = venusian.attach(wrapped, self.callback, 'pyramid', depth=depth)
        self.module = info.module
        return wrapped


class ViewDecorator(BaseDecorator):
    """Base class for HTTP request method decorators for resources.

    This class should never be used directly. It is used internally to create
    the ``DELETE``, ``GET``, ``OPTIONS``, ``PATCH``, ``POST`` and ``PUT``
    decorators for resources classes when the :py:func:`resource` decorator is
    used.

    .. code-block:: python
       :linenos:

       @MyResource.GET()
       def get_view_for_my_resource(resource, request):
           '''Handle GET requests for MyResource.
           '''
    """
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
                context=self.state.resource_class,
                **self.view_arguments)


class ControllerDecorator(BaseDecorator):
    """Base class for controller views for resources.

    This class should never be used directly. It is used internally to create
    the `controller`decorator for resources classes when the
    :py:func:`resource` decorator is used.

    .. code-block:: python
       :linenos:

       @MyResource.controller('frobnicate')
       def frobnicate_my_resource(resource, request):
           '''Handle POST requests to ``/myresource/frobnicate``
           '''
   """
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
        config.add_view(unsupported_method_view, route_name=route_name, renderer='json')
        config.add_view(view,
                route_name=route_name,
                request_method='POST',
                context=self.state.resource_class,
                **self.view_arguments)


class resource(BaseDecorator):
    """Configure a REST resource.

    This decorator must be used to declare REST resources.

    .. code-block:: python
       :linenos:

       from rest_toolkit import resource

       @resource('/users/{id}')
       class User:
           def __init__(self, request):
               self.user_id = request.matchdict['id']


    :param route_path: The URL route pattern to use for the resource.

       For more information on route patterns please see the :ref:`Pyramid
       route pattern syntax <pyramid:route_pattern_syntax>` documentation.
    """
    def __init__(self, pattern):
        self.route_path = pattern

    def callback(self, scanner, name, cls):
        state = RestState.from_resource(cls)
        config = scanner.config.with_package(self.module)
        route_name = state.route_name()
        config.add_route(route_name, state.route_path, factory=cls)
        config.add_view(default_options_view, route_name=route_name,
                request_method='OPTIONS')
        config.add_view(unsupported_method_view, route_name=route_name, renderer='json')
        for (method, base_class, view) in [
                ('DELETE', DeletableResource, default_delete_view),
                ('GET', ViewableResource, default_get_view),
                ('PATCH', EditableResource, default_patch_view),
                ('PUT', EditableResource, default_put_view)]:
            config.add_view(view,
                    route_name=route_name,
                    context=base_class,
                    renderer='json',
                    request_method=method)

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
    """Configure basic REST settings for a Pyramid application.

    You should not call this function directly, but use
    :py:func:`pyramid.config.Configurator.include` to initialise
    the REST toolkit.

    .. code-block:: python
       :linenos:

       config = Configurator()
       config.include('rest_toolkit')
    """
    config.add_view('rest_toolkit.error.generic', context=Exception, renderer='json')
    config.add_view('rest_toolkit.error.http_error', context=IExceptionResponse, renderer='json')
    config.add_view('rest_toolkit.error.http_error', context=WSGIHTTPException, renderer='json')
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
       :linenos:

       from pyramid.config import Configurator
       from wsgiref.simple_server import make_server

       config = Configurator()
       config.include('rest_toolkit')
       config.scan()
       app = config.make_wsgi_app()
       make_server('0.0.0.0', 8080, app).serve_forever()

    :param sql_session_factory: A factory function to return a SQLAlchemy
        session. This is generally a :py:class:`scoped_session
        <sqlalchemy:sqlalchemy.orm.session.scoped_session>` instance, and
        commonly called ``Session`` or ``DBSession``.
    :param int port: TCP port to use for HTTP server.
    """
    config = Configurator()
    config.include('rest_toolkit')
    if sql_session_factory is not None:
        config.include('rest_toolkit.ext.sql')
        config.set_sqlalchemy_session_factory(sql_session_factory)
    pkg = caller_package()
    config.add_static_view('static', package_path(pkg))
    config.scan(pkg)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()


__all__ = ['resource', 'quick_serve']
