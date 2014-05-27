import pytest
from webtest import TestApp


def make_app(config):
    return TestApp(config.make_wsgi_app())


@pytest.mark.parametrize('method', ['delete', 'get', 'post', 'put'])
def test_unallowed_method_added(config, method):
    config.scan('resource_only')
    app = make_app(config)
    getattr(app, method)('/', status=405)


def test_default_options_method(config):
    config.scan('resource_only')
    app = make_app(config)
    response = app.options('/')
    assert response.headers['Access-Control-Allow-Methods'] == 'OPTIONS'
