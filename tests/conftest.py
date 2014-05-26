import pytest
import pyramid.testing
from webtest import TestApp


@pytest.fixture
def config(request):
    request.addfinalizer(pyramid.testing.tearDown)
    return pyramid.testing.setUp()


@pytest.fixture
def app(config):
    app = config.make_wsgi_app()
    return TestApp(app)
