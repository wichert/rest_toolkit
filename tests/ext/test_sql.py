import pytest
from webtest import TestApp
from pyramid.config import Configurator
from pyramid.testing import DummyRequest
from pyramid_sqlalchemy import Session
from resource_sql import BalloonModel
from resource_sql import BalloonResource
from rest_toolkit.ext.sql import _column_keys


def make_app(config):
    return TestApp(config.make_wsgi_app())


def test_column_keys():
    keys = _column_keys(BalloonResource.context_query)
    assert set(keys) == {(True, 'id'), (False, 'figure')}


@pytest.mark.usefixtures('sql_session')
def test_unknown_id():
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_sql')
    app = make_app(config)
    r = app.get('/balloons/1', status=404)


@pytest.mark.usefixtures('sql_session')
def test_known_id():
    balloon = BalloonModel(figure=u'Giraffe')
    Session.add(balloon)
    Session.flush()
    config = Configurator()
    config.include('rest_toolkit')
    config.scan('resource_sql')
    app = make_app(config)
    r = app.get('/balloons/%s' % balloon.id)
    assert r.json['figure'] == u'Giraffe'


@pytest.mark.usefixtures('sql_session')
def test_update_instance():
    balloon = BalloonModel(figure=u'Giraffe')
    Session.add(balloon)
    Session.flush()
    request = DummyRequest(matchdict={'id': balloon.id})
    resource = BalloonResource(request)
    resource.update_from_dict({'figure': u'Elephant'})
    assert balloon.figure == u'Elephant'
