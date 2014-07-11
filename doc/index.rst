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
   :linenos:

   from rest_toolkit import quick_serve
   from rest_toolkit import resource


   @resource('/')
   class Root(object):
       def __init__(self, request):
           pass

   @Root.GET()
   def show_root(root, request):
       return {'status': 'OK'}


   if __name__ == '__main__':
       quick_serve()


The previous example is simple, but real REST services are likely to be
much more complex, for example because they need to request data from a
SQL server. The next example shows how you can use SQL data.


.. code-block:: python
   :linenos:

   from rest_toolkit import quick_serve
   from rest_toolkit import resource
   from rest_toolkit.ext.sql import SQLResource
   from sqlalchemy import Column, Integer, String, bindparam
   from sqlalchemy.orm import Query
   from pyramid_sqlalchemy import BaseObject
   from pyramid_sqlalchemy import DBSession


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
                         for user in DBSession.query(User)]}


   @resource('/users/{id}')
   class UserResource(SQLResource):
       context_query = Query(User) .filter(User.id == bindparam('id'))


   @UserResource.GET()
   def show_user(user, request):
       return {'id': user.id, 'fullname': user.fullname}


   if __name__ == '__main__':
       quick_serve(DBSession)

This example creates two resources: a ``/users`` collection which will return a
list of all users for a ``GET``-request, and a ``/users/<id>`` resource which
will return information for an individual user on a ``GET``-request.


Contents
========

.. toctree::
   :maxdepth: 2

   basics
   sql
   security
   philosophy
   api
   comparison
   changes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
