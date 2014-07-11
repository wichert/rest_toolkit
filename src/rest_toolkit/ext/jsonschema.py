from __future__ import absolute_import
import abc
import jsonschema
from pyramid.httpexceptions import HTTPBadRequest
from ..compat import add_metaclass
from ..utils import merge


@add_metaclass(abc.ABCMeta)
class JsonSchemaValidationMixin(object):
    """Mix-in class to add JSON schema validation to a resource.

    This mix-in class provides an implementation for :py:meth:`validate`
    as required by :py:class:`EditableResource
    <rest_toolkit.abc.EditableResource>` which uses `JSON schemas
    <http://json-schema.org/>`).

    .. code-block:: python
       :linenos:

       class Account(EditableResource, JsonSchemaValidationMixin):
           schema = {
                   '$schema': 'http://json-schema.org/draft-04/schema',
                   'type': 'object',
                   'properties': {
                       'email': {
                           'type': 'string',
                           'format': 'email',
                        },
                        'password'': {
                            'type': 'string',
                            'minLength': 1,
                        },
                    },
                    'additionalProperties': False,
                    'required': ['email', 'password'],
            }

    The `jsonschema <https://pypi.python.org/pypi/jsonschema>`_ package is used
    to implement validation. All validation errors reported by jsonschema are
    returned as a standard error JSON response with HTTP status code 400.
    """

    @abc.abstractproperty
    def schema(self):
        """JSON schema.

        This attribute must contain s valid JSON schema. This will be used by
        :py:meth:`validate` to validate submitted data.
        """
        raise NotImplemented()

    def validate(self, data, partial=False):
        if partial:
            data = merge(self.to_dict(), data)
        try:
            jsonschema.validate(data, self.schema,
                format_checker=jsonschema.draft4_format_checker)
        except jsonschema.ValidationError as e:
            raise HTTPBadRequest(e.message)


__all__ = ['JsonSchemaValidationMixin']
