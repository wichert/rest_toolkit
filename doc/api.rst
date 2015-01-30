API documentation
=================

rest_toolkit
------------

.. module:: rest_toolkit

.. autofunction:: includeme

.. autofunction:: quick_serve

.. autoclass:: resource

.. autoclass:: ViewDecorator

.. autoclass:: ControllerDecorator


rest_toolkit.abc
----------------

.. module:: rest_toolkit.abc

.. autoclass:: DeletableResource
   :members:

.. autoclass:: EditableResource
   :members:

.. autoclass:: ViewableResource
   :members:


rest_toolkit.utils
------------------

.. module:: rest_toolkit.utils

.. autofunction:: merge



rest_toolkit.ext.colander
---------------------------

.. module:: rest_toolkit.ext.colander

.. autoclass:: ColanderSchemaValidationMixin
   :members:

.. autofunction:: validate


rest_toolkit.ext.jsonschema
---------------------------

.. module:: rest_toolkit.ext.jsonschema

.. autoclass:: JsonSchemaValidationMixin
   :members:

.. autofunction:: validate


rest_toolkit.ext.sql
--------------------

.. module:: rest_toolkit.ext.sql

.. autoclass:: SQLResource
   :members:

.. autofunction:: set_sqlalchemy_session_factory

.. autofunction:: includeme
