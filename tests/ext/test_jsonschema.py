import pytest
from pyramid.httpexceptions import HTTPBadRequest
from rest_toolkit.abc import EditableResource
from rest_toolkit.ext.jsonschema import JsonSchemaValidationMixin


class DummyResource(JsonSchemaValidationMixin, EditableResource):
    schema = {
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
               'groups': {
                   'type': 'array',
                   'items': {
                       'type': 'string',
                       'enum': ['admin', 'user'],
                    },
                },
           },
           'additionalProperties': False,
           'required': ['email', 'password'],
    }

    def to_dict(self):
        return {}

    def update_from_dict(self, data, partial):
        pass


def test_valid_request():
    resource = DummyResource()
    resource.validate({'email': 'john@example.com', 'password': 'Jane'}, partial=False)


def test_validation_error():
    resource = DummyResource()
    with pytest.raises(HTTPBadRequest):
        resource.validate({'email': 'john@example.com'}, partial=False)


def test_array_validation_error():
    resource = DummyResource()
    with pytest.raises(HTTPBadRequest):
        resource.validate({
                'email': 'john@example.com',
                'password': 'Jane',
                'groups': ['admin', 'invalid'],
            }, partial=False)


def test_multiple_errors():
    resource = DummyResource()
    with pytest.raises(HTTPBadRequest) as exc_info:
        import pdb ; pdb.set_trace()
        resource.validate({})
    assert 'email' in exc_info.value.json
    assert 'password' in exc_info.value.json


def test_partial_data():
    resource = DummyResource()
    resource.to_dict = lambda: {'password': 'Jane'}
    resource.validate({'email': 'john@example.com'}, partial=True)
