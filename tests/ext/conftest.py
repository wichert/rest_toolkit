import mock
import pytest
from sqlalchemy import create_engine
from pyramid_sqlalchemy import Session
from pyramid_sqlalchemy import metadata
from pyramid_sqlalchemy import init_sqlalchemy


def pytest_addoption(parser):
    parser.addoption('--sql-url', default='sqlite:///',
            help='SQLAlchemy Database URL')
    parser.addoption('--sql-echo', default=False, action='store_true',
            help='Echo SQL statements to console')


def pytest_generate_tests(metafunc):
    if 'sqlalchemy_url' in metafunc.fixturenames:
        metafunc.parametrize('sqlalchemy_url', [metafunc.config.option.sql_url], scope='session')
    if 'sql_echo' in metafunc.fixturenames:
        metafunc.parametrize('sql_echo', [metafunc.config.option.sql_echo], scope='session')


@pytest.yield_fixture(scope='session')
def _sqlalchemy(sqlalchemy_url, sql_echo):
    engine = create_engine(sqlalchemy_url, echo=sql_echo)
    if engine.dialect.name == 'sqlite':
        engine.execute('PRAGMA foreign_keys = ON')
    # Check if a previous test has kept a session open. This will silently
    # make Session.configure do nothing and then break all our tests.
    assert not Session.registry.has()
    init_sqlalchemy(engine)
    metadata.create_all(engine)

    yield Session()

    Session.remove()
    metadata.drop_all(engine)
    Session.configure(bind=None)
    metadata.bind = None
    engine.dispose()


@pytest.yield_fixture
def transaction():
    import transaction
    tx = transaction.begin()
    tx.doom()  # Make sure a transaction can never be commited.
    # Mock out transaction.get so code can call abort
    with mock.patch('transaction.get'):
        yield
    tx.abort()


@pytest.fixture
def sqlalchemy(transaction, _sqlalchemy):
    return _sqlalchemy
