from webtest import TestApp
from pyramid.config import Configurator


def make_app(config):
    return TestApp(config.make_wsgi_app())


def test_resource_constructor_exception():
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_error')
    app = make_app(config)
    r = app.get('/keyerror', status=500)
    assert r.content_type == 'application/json'
    assert set(r.json) == {'message'}
    assert r.json['message'] == 'BOOM!'


def test_resource_constructor_http_exception():
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_error')
    app = make_app(config)
    r = app.get('/http-error', status=404)
    assert r.content_type == 'application/json'
    assert set(r.json) == {'message'}
    assert r.json['message'] == 'BOOM!'


def test_notfound_response():
    config = Configurator()
    config.include('rest_toolkit')
    app = make_app(config)
    r = app.get('/', status=404)
    assert r.content_type == 'application/json'
    assert set(r.json) == {'message'}
