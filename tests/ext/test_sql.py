import pytest
from webtest import TestApp
from pyramid.config import Configurator
from resource_sql import BalloonModel
from pyramid_sqlalchemy import Session


def make_app(config):
    return TestApp(config.make_wsgi_app())


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
