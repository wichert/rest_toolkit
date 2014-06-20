Introduction
============

*rest_toolkit* is a Python package which provides a very convenient way to
build REST servers. It is build on top of
`Pyramid <http://www.pylonsproject.org/projects/pyramid/about>`_, but you do not
need to know much about Pyramid to use rest_toolkit.


Quick example
=============

This is a minimal example which defines a ``Root`` resource with a ``GET``
view, and starts a simple HTTP server. If you run this example you can request
``http://localhost:8080/`` and you will see a JSON response with a status
message.

.. code-block:: python

   from wsgiref.simple_server import make_server
   from rest_toolkit import resource
   from pyramid.config import Configurator


   @resource('/')
   class Root(object):
       def __init__(self, request):
           pass

   @Root.GET()
   def show_root(root, request):
       return {'status': 'OK'}


   if __name__ == '__main__'
       config = Configurator()
       config.scan()
       app = config.make_wsgi_app()
       server = make_server('0.0.0.0', 8080, app)
       server.serve_forever()


The previous example is simple, but real REST services are likely to be
much more complex, for example because they need to request data from a
SQL server. The next example shows how you can use SQL data.


.. code-block:: python

   from wsgiref.simple_server import make_server
   from rest_toolkit import resource
   from sqlalchemy import Column, Integer, String
   from pyramid_sqlalchemy import BaseObject
   from pyramid_sqlalchemy import Session
   from pyramid.config import Configurator
   
   
   class User(BaseObject):
       __tablename__ = 'user'
       id = Column(Integer, primary_key=True)
       fullname = Column(String)
   
   
   @resource('/users')
   class UserCollection(object):
       def __init__(self, request):
           pass
   
   
   @UserCollection.GET()
   def list_users(collection, request):
       return {'users': [{'id': user.id,
                          'fullname': user.fullname}
                         for user in Session.query(User)]}
   
   
   @resource('/users/{id}')
   class UserResource(SQLResource):
       context_query = sqlalchemy.orm.Query(User)\
           .filter(User.id == sqlalchemy.bindparam('id'))
   

   @UserResource.GET()
   def show_user(user, request):
       return {'id': user.id, 'fullname': user.fullname}
   
   
   if __name__ == '__main__':
       config = Configurator()
       config.scan()
       app = config.make_wsgi_app()
       server = make_server('0.0.0.0', 8080, app)
       server.serve_forever()

This example creates two resources: a ``/users`` collection which will return a
list of all users for a ``GET``-request, and a ``/users/<id>`` resource which
will return information for an individual user on a ``GET``-request.


Contents
========

.. toctree::
   :maxdepth: 2

   basics
   philosophy
   comparison



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
