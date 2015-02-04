import pytest
from pyramid.httpexceptions import HTTPBadRequest
from rest_toolkit.abc import EditableResource
from rest_toolkit.ext.colander import ColanderSchemaValidationMixin
import colander


class AccountSchema(colander.Schema):
    email = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String())


class DummyResource(ColanderSchemaValidationMixin, EditableResource):
    schema = AccountSchema

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


def test_partial_data():
    resource = DummyResource()
    resource.to_dict = lambda: {'password': 'Jane'}
    resource.validate({'email': 'john@example.com'}, partial=True)
