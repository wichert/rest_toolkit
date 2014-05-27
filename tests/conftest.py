import pytest
import pyramid.testing


@pytest.fixture
def config(request):
    request.addfinalizer(pyramid.testing.tearDown)
    return pyramid.testing.setUp()
