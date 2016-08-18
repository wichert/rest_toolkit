from __future__ import absolute_import
import abc
import jsonschema
from pyramid.httpexceptions import HTTPBadRequest
from ..compat import add_metaclass
from ..utils import add_missing


class JSONValidationError(HTTPBadRequest):
    """HTTP response for JSON validation errors.
    """

def validate(data, schema):
    """Validate data against a JSON schema.

    This is a helper function used by :py:class:`JsonSchemaValidationMixin`
    to validate data against a JSON schema. If validation fails this function
    will raise a :py:class:`pyramid.httpexceptions.HTTPBadRequest` exception
    describing the validation error.

    :raises pyramid.httpexceptions.HTTPBadRequest: if validation fails this
        exception is raised to abort any further processing.
    """
    try:
        jsonschema.validate(data, schema,
            format_checker=jsonschema.draft4_format_checker)
    except jsonschema.ValidationError as e:
        error = {
            '.'.join(e.path): e.message
        }
        response = JSONValidationError(json=error)
        response.validation_error = e
        raise response


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
                        'password': {
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

        This attribute must contain a valid JSON schema. This will be used by
        :py:meth:`validate` to validate submitted data.
        """
        raise NotImplemented()

    def validate(self, data, partial=False):
        if partial:
            data = self.complete_partial_data(data)
        validate(data, self.schema)


@add_metaclass(abc.ABCMeta)
class JsonSchemaChildValidationMixin(object):
    """Mix-in class to add JSON schema validation to a resource.

    This mix-in class provides an implementation for :py:meth:`validate_child`
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
                        'password': {
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
    def child_schema(self):
        """JSON schema.

        This attribute must contain a valid JSON schema. This will be used by
        :py:meth:`validate` to validate submitted data.
        """
        raise NotImplemented()

    def validate_child(self, data):
        validate(data, self.child_schema)


__all__ = ['JsonSchemaValidationMixin', 'JsonSchemaChildValidationMixin', 'validate']
