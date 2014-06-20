_session_factory = None


class SQLResource(object):
    """Base class for resources based on SQLAlchemy ORM models.

    """

    #: A SQLAlchemy query which is used to find a SQLAlchemy object.
    context_query = None

    def __init__(self, request):
        global _session_factory
        assert _session_factory is not None, \
                "config.set_sqlalchemy_session_factory must be called."
        params = request.matchdict
        self.context = _session_factory.execute(self.context_query, params).first()
        if self.context is None:
            raise KeyError('Resource not found')


def set_sqlalchemy_session_factory(config, factory):
    """Configure the SQLAlchemy session factory.
    """
    global _session_factory
    _session_factory = factory


def includeme(config):
    config.add_directory('set_sqlalchemy_session_factory',
            set_sqlalchemy_session_factory)
