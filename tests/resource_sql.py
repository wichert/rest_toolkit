from rest_toolkit import resource
from rest_toolkit.abc import ViewableResource
from rest_toolkit.ext.sql import SQLResource
from pyramid_sqlalchemy import BaseObject
from sqlalchemy import bindparam
from sqlalchemy.orm import Query
from sqlalchemy import schema
from sqlalchemy import types


class BalloonModel(BaseObject):
    __tablename__ = 'balloon'

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    figure = schema.Column(types.Unicode(), nullable=False)


@resource('/balloons/{id}')
class BalloonResource(SQLResource, ViewableResource):
    context_query = Query(BalloonModel)\
            .filter(BalloonModel.id == bindparam('id'))
