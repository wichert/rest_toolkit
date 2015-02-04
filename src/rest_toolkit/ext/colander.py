from __future__ import absolute_import
import abc
from pyramid.httpexceptions import HTTPBadRequest
import colander
from ..compat import add_metaclass


def validate(data, schema):
    """Validate data against a Colander schema class.

    This is a helper function used by :py:class:`ColanderSchemaValidationMixin`
    to validate data against a Colander schema. If validation fails this function
    will raise a :py:class:`pyramid.httpexceptions.HTTPBadRequest` exception
    describing the validation error.

    :raises pyramid.httpexceptions.HTTPBadRequest: if validation fails this
        exception is raised to abort any further processing.
    """
    schema_instance = schema()
    try:
        schema_instance.deserialize(data)
    except colander.Invalid as e:
        raise HTTPBadRequest(e.msg)


@add_metaclass(abc.ABCMeta)
class ColanderSchemaValidationMixin(object):
    """Mix-in class to add colander-based validation to a resource.

    This mix-in class provides an implementation for :py:meth:`validate`
    as required by :py:class:`EditableResource
    <rest_toolkit.abc.EditableResource>` which uses `colander
    <http://colander.readthedocs.org/>`_ for validation.

    .. code-block:: python
       :linenos:

       class AccountSchema(colander.Schema):
           email = colander.SchemaNode(colander.String())
           password = colander.SchemaNode(colander.String())
   
   
       class DummyResource(ColanderSchemaValidationMixin):
           schema = AccountSchema

    """

    @abc.abstractproperty
    def schema(self):
        """Colander schema class.
        """
        raise NotImplemented()

    def validate(self, data, partial=False):
        if partial:
            data = self.complete_partial_data(data)
        validate(data, self.schema)


__all__ = ['ColanderSchemaValidationMixin', 'validate']
