SQL support
===========

*rest_toolkit* has a SQL-extension that makes it easy to use `SQLAlchemy
<http://www.sqlalchemy.org/>`_ models in your REST application. 

In line with rest_toolkit's :ref:`philosophy <philosophy-chapter>` a SQLAlchemy
model is not used directly as a resource. Instead a `SQLResource` class is used
which wraps a SQL model. This resource class can define things like the
:ref:`ACLs <pyramid:assigning_acls>` and methods needed for :ref:`default views
<default-views>`. This keeps a clean separation between the data model and
related business logic and the frontend.


Setup
-----

The toolkit assumes you are using `pyramid_sqlalchemy
<https://pyramid-sqlalchemy.readthedocs.org>`_ to handle the SQLAlchemy
integration. If you do not use pyramid_sqlalchemy you will need to point the
SQL extension to your session factory. This is done during application
initialisation via the ``config`` object:

.. code-block:: python
   :linenos:

   config = Configurator()
   config.include('rest_toolkit')
   config.include('rest_toolkit.ext.sql')
   config.set_sqlalchemy_session_factory(DBSession)

The ``DBSession`` object is the SQLAlchemy session maker. This is usually
called ``DBSession`` or ``Sesssion``. Again, this is only necessary if you
do not use pyramid_sqlalchemy.


Defining a resource
-------------------

Once you have done this you can use the :py:class:`SQLResource
<rest_toolkit.ext.sql.SQLResource>` class to define your resources.

.. code-block:: python
   :linenos:

   from sqlalchemy import bindparam
   from sqlalchemy.orm import Query
   from rest_toolkit.ext.sql import SQLResource

   
   @resource('/users/{id}')
   class UserResource(SQLResource):
       context_query = Query(User).filter(User.id == bindparam('id'))


   @UserResource.GET()
   def view_user(resource, request):
       user = resource.context  # Get the SQLAlchemy model from the resource
       return {'id': user.id,
               'name': user.full_name}

Line 4 defines the URL path for the resource. This path includes an
``id``-variable, which will be used in a SQL query. The query is defined in
line 6. This query uses a :py:func:`bound expression
<sqlalchemy:sqlalchemy.sql.expression.bindparam>` to specify where the
``id`` request variable must be used.

When a request comes in for ``/users/123`` a number of things will happen
internally:

1. The ``id`` will be extracted from the URL path. In this case the resulting
   id is ``123``.
2. The SQL query specified in ``context_query`` is executed, with the ``id``
   variable from the request passed in.
3. If the SQL query returns a single response it is assigned to the ``context``
   variable of the ``UserResource`` instance. If the SQL query did not return
   any results or returned more than one result a HTTP 404 error will be
   generated directly.


Default views
-------------

SQLResource support default views, but does automatically enable them to
prevent accidental data exposure or edit/delete functionality.

To enable the default GET view for a SQL resource you only need to add
:py:class:`ViewableResource <rest_toolkit.abc.ViewableResource>` to the
list of base classes. SQLResource includes a default `to_dict` method which
returns a dictionary with all column defined in the SQLAlchemy model used in
`context_query`, which will be used to generate the response for GET requests.

.. code-block:: python
   :linenos:

   from rest_toolkit.abc import ViewableResource
   from rest_toolkit.ext.sql import SQLResource

   @resource('/users/{id}')
   class UserResource(SQLResource, ViewableResource):
       context_query = Query(User).filter(User.id == bindparam('id'))

.. warning::

   It is important that when defining your class you list the SQLResource
   class *before* ViewableResource or any of the other base classes for
   default views. If you do not do this you will get a Python error on
   application startup.

There is also a default `delete` method which deletes the SQL object from
the database. To expose those you can add
:py:class:`DeletableResource <rest_toolkit.abc.DeletableResource>` to the
base classes for your resource.

There is also a default implementation of the `update_from_dict` method which
can be used as part of the 
:py:class:`EditableResource <rest_toolkit.abc.EditableResource>` interface.
You must supply an implementation for `validate` yourself.

.. code-block:: python
   :linenos:

   from rest_toolkit.abc import EditableResource
   from rest_toolkit.ext.sql import SQLResource

   @resource('/users/{id}')
   class UserResource(SQLResource, EditableResource):
       context_query = Query(User).filter(User.id == bindparam('id'))

       def validate(self, data, partial):
           # Validate data here

The default update logic will not update and primary keys. If you want to allow
key changes you can set the ``allow_primary_key_change`` class attribute.


.. code-block:: python
   :linenos:

   from rest_toolkit.abc import EditableResource
   from rest_toolkit.ext.sql import SQLResource

   @resource('/users/{id}')
   class UserResource(SQLResource, EditableResource):
       context_query = Query(User).filter(User.id == bindparam('id'))

       allow_primary_key_change = True

