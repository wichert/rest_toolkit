from __future__ import absolute_import
import abc
from pyramid.httpexceptions import HTTPBadRequest
import colander
from ..compat import add_metaclass
from ..utils import merge


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
        """Colander schema class
        """
        raise NotImplemented()

    def validate(self, data, partial=False):
        schema = self.schema()
        if partial:
            data = merge(self.to_dict(), data)
        try:
            schema.deserialize(data)
        except colander.Invalid as e:
            raise HTTPBadRequest(e.msg)
