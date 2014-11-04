import pytest
from webtest import TestApp
from pyramid.config import Configurator
from pyramid.testing import DummyRequest
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy


def make_app(config):
    return TestApp(config.make_wsgi_app())


@pytest.mark.parametrize('method', ['delete', 'get', 'post', 'patch', 'put'])
def test_unallowed_method_added(method):
    config = Configurator()
    config.scan('resource_only')
    app = make_app(config)
    getattr(app, method)('/', status=405)


def test_default_options_method():
    config = Configurator()
    config.scan('resource_only')
    app = make_app(config)
    response = app.options('/')
    assert response.headers['Access-Control-Allow-Methods'] == 'OPTIONS'


def test_request_add_get_view():
    config = Configurator()
    config.scan('resource_get')
    app = make_app(config)
    app.get('/')


def test_request_default_to_json_renderer():
    config = Configurator()
    config.scan('resource_get')
    app = make_app(config)
    r = app.get('/')
    assert r.content_type == 'application/json'
    assert r.json == {'message': 'hello'}


def test_request_override_renderer():
    config = Configurator()
    config.scan('resource_get_renderer')
    app = make_app(config)
    r = app.get('/')
    assert r.content_type == 'text/plain'
    assert r.unicode_body == 'hello'


def test_add_controller():
    config = Configurator()
    config.scan('controller')
    app = make_app(config)
    app.post('/engage')


def test_nested_controller():
    # Test for https://github.com/wichert/rest_toolkit/issues/12
    config = Configurator()
    config.scan('controller')
    app = make_app(config)
    app.post('/resource/engage')


def test_controller_default_to_json_renderer():
    config = Configurator()
    config.scan('controller')
    app = make_app(config)
    r = app.post('/engage')
    assert r.content_type == 'application/json'
    assert r.json == {'message': 'Ai ai captain'}


def test_set_controller_method():
    config = Configurator()
    config.scan('controller')
    app = make_app(config)
    r = app.get('/engage')
    assert r.json == {'message': 'Warp engine offline'}


@pytest.mark.parametrize('method', ['delete', 'get', 'patch', 'put'])
def test_controller_invalid_method(method):
    config = Configurator()
    config.scan('controller')
    app = make_app(config)
    getattr(app, method)('/', status=405)


def test_default_get_view():
    config = Configurator()
    config.scan('resource_abc')
    app = make_app(config)
    r = app.get('/')
    assert r.json == {'message': 'Hello, world'}


def test_override_default_view():
    config = Configurator()
    config.scan('resource_abc_override')
    app = make_app(config)
    r = app.get('/')
    assert r.json == {'message': 'Welcome'}


def test_set_resource_route_name():
    config = Configurator()
    config.scan('resource_route_name')
    config.make_wsgi_app()
    request = DummyRequest()
    request.registry = config.registry
    assert request.route_path('user', id=15) == '/users/15'


def test_secured_default_view_not_allowed():
    config = Configurator()
    config.set_authentication_policy(AuthTktAuthenticationPolicy('seekrit'))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.scan('resource_abc')
    app = make_app(config)
    app.get('/secure', status=403)


def test_secured_default_view_allowed():
    config = Configurator()
    config.testing_securitypolicy(1)
    config.scan('resource_abc')
    app = make_app(config)
    app.get('/secure')
