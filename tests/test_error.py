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
    assert 'traceback' not in r.json


def test_add_traceback_in_debug_mode():
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_error')
    config.registry.settings['rest_toolkit.debug'] = True
    app = make_app(config)
    r = app.get('/keyerror', status=500)
    assert 'traceback' in r.json


def test_resource_constructor_http_exception():
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_error')
    app = make_app(config)
    r = app.get('/http-error', status=402)
    assert r.content_type == 'application/json'
    assert set(r.json) == {'message'}
    assert r.json['message'] == 'BOOM!'


def test_resource_constructor_raises_notfound():
    config = Configurator()
    config.include('rest_toolkit')
    config.include('pyramid_tm')
    app = make_app(config)
    r = app.get('/http-not-found', status=404)
    assert r.content_type == 'application/json'
    assert set(r.json) == {'message'}


def test_preserve_custom_json_response():
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_error')
    app = make_app(config)
    r = app.get('/custom-json-exception', status=400)
    assert r.content_type == 'application/json'
    assert r.json == {'foo': 'bar'}



def test_notfound_response():
    config = Configurator()
    config.include('rest_toolkit')
    app = make_app(config)
    r = app.get('/', status=404)
    assert r.content_type == 'application/json'
    assert set(r.json) == {'message'}


def test_found_exception():
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_error')
    app = make_app(config)
    r = app.get('/http-found', status=302)
    assert r.headers['Location'] == 'http://www.wiggy.net'
    assert r.content_type == 'application/json'
    assert set(r.json) == {'message'}


def test_method_not_allowed():
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_get')
    app = make_app(config)
    r = app.put('/', status=405)
    assert r.content_type == 'application/json'
    assert set(r.json) == {'message'}
