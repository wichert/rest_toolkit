import abc
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm import object_session
from ..compat import add_metaclass

try:
    from pyramid_sqlalchemy import Session as _session_factory
except ImportError:  # pragma: noqa
    _session_factory = None


def _column_keys(query):
    return [(column.primary_key, column.key) for column in query._primary_entity.entity_zero.columns]


@add_metaclass(abc.ABCMeta)
class SQLResource(object):
    """Base class for resources based on SQLAlchemy ORM models.
    """

    allow_primary_key_change = False

    @abc.abstractproperty
    def context_query(self):
        """A SQLAlchemy query which is used to find a SQLAlchemy object.
        """
        raise NotImplemented()

    def __init__(self, request):
        global _session_factory
        assert _session_factory is not None, \
                "config.set_sqlalchemy_session_factory must be called."
        self.request = request
        self.context = self.context_query\
                .with_session(_session_factory())\
                .params(request.matchdict)\
                .first()
        if self.context is None:
            raise HTTPNotFound('Resource not found')

    def to_dict(self):
        data = {}
        for (_, column) in _column_keys(self.context_query):
            data[column] = getattr(self.context, column)
        return data

    def update_from_dict(self, data, replace=False):
        for (key, column) in _column_keys(self.context_query):
            if key and not self.allow_primary_key_change:
                continue
            if not replace:
                setattr(self.context, column, data.get(column))
            else:
                setattr(self.context, column, data[column])

    def delete(self):
        object_session(self.context).delete(self.context)


def set_sqlalchemy_session_factory(config, sql_session_factory):
    """Configure the SQLAlchemy session factory.

    This function should not be used directly, but as a method if the
    ``config`` object.

    .. code-block:: python
       :linenos:

       config.set_sqlalchemy_session_factory(DBSession)

    This function must be called if you use SQL resources. If you forget to do
    this any attempt to access a SQL resource will trigger an assertion
    exception.

    :param sql_session_factory: A factory function to return a SQLAlchemy
        session. This is generally a :py:class:`scoped_session
        <sqlalchemy:sqlalchemy.orm.session.scoped_session>` instance, and
        commonly called ``Session`` or ``DBSession``.
    """
    global _session_factory
    _session_factory = sql_session_factory


def includeme(config):
    """Configure SQLAlchemy integration.

    You should not call this function directly, but use
    :py:func:`pyramid.config.Configurator.include` to initialise the REST
    toolkit. After you have done this you must call
    :py:func:`config.set_sqlalchemy_session_factory` to register your
    SQLALchemy session factory.

    .. code-block:: python
       :linenos:

       config = Configurator()
       config.include('rest_toolkit')
       config.include('rest_toolkit.ext.sql')
       config.set_sqlalchemy_session_factory(DBSession)
    """
    config.add_directive('set_sqlalchemy_session_factory',
            set_sqlalchemy_session_factory)
