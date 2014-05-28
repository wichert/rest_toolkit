*rest_toolkit* is a Python package which provides a very convenient way to
build REST servers. It is build on top of
[Pyramid](http://www.pylonsproject.org/projects/pyramid/about), but you do not
need to know much about Pyramid to use rest_toolkit.

Examples
========

This is a minimal example which defines a `Root` resource with a `GET` view,
and starts a simple HTTP server. If you run this example you can request
`http://localhost:8080/` and you will see a JSON response with a status
message.

```python
from wsgiref.simple_server import make_server
from rest_toolkit import resource
from pyramid.config import Configurator


@resource('/')
class Root(object):
    def __init__(self, request):
        pass

@Root.GET()
def show_root(root, request):
    return {'status': 'OK'}


config = Configurator()
config.scan()
app = config.make_wsgi_app()
server = make_server('0.0.0.0', 8080, app)
server.serve_forever()
```

The previous example is simple, but real REST services are likely to be
much more complex, for example because they need to request data from a
SQL server. The next example shows how you can use SQL data.


```python
from wsgiref.simple_server import make_server
from rest_toolkit import resource
from sqlalchemy import Column, Integer, String
from pyramid_sqlalchemy import BaseObject
from pyramid_sqlalchemy import Session
from pyramid.config import Configurator


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
		       for user in Session.query(User)]}


@resource('/users/{id}')
class UserResource(SQLResource):
    context_query = sqlalchemy.orm.Query(User)\
        .filter(User.id==sqlalchemy.bindparam(‘id’))

@UserResource.GET()
def show_user(user, request):
    return {'id': user.id, 'fullname': user.fullname}


config = Configurator()
config.scan()
app = config.make_wsgi_app()
server = make_server('0.0.0.0', 8080, app)
server.serve_forever()
```

This example creates two resources: a `/users` collection which will
return a list of all users for a `GET`-request, and a `/users/<id>` resource
which will return information for an individual user on a `GET`-request.


Philosphy
=========

*rest_toolkit* tries to follow the standard
[REST](http://en.wikipedia.org/wiki/Representational_state_transfer) standards
for HTTP as much as possible:

* every URL uniquely identifies a *resource*
* an `OPTIONS` request must return the list of supported request methods in an
  `Access-Control-Allow-Methods` header.
* a request using an unsupported request method must return a HTTP 405 error.

A resource typically corresponds to something stored in a database. The mapping
does not need to be one-to-one: stored data can be exposed at multiple places
by an API, and each location is a separate resource from a REST point of view.
For example in an event management system a user can see see event information
in a list of events he has registered for as `/users/12/events/13`, while an
event staff member manages the event via a `/events/13`. Both URLs will use the
same event object in the database, but are separate REST resources, and will
return different data, use a different ACL, etc.

 *rest_toolkit* follows this philosophy ant matches URLs to resources instead
 of stored data. This has several advantages:

* your data model does not need to be aware of frontend-specific things like
  access control lists or JSON formatting.
* you can easily present the same data in multiple ways.



Three types of resources:

1. Element: a single entity, for example a user.
2. Collection: a collection of entities, for example the list of all known users.
3. Controller: a resource which only performs some action. Typically a controller
   only response to a `POST` request.



Defining a resource
-------------------

```python
from pyramid_rest import Resource
from .models import DBSession
from .models import Event


@resource(route_path='/events/{id:\d+}')
class EventResource(object):
    def __init__(self, request):
        event_id = request.matchdict['id']
        self.event = DBSession.query(Event).get(event_id)
        if self.event is None:
            raise KeyError('Unknown event id')
```

As you can see this the `resource` decorator is essentially a convenient way to
setup configure a route with a context factory. The `Resource` base class adds
some extra behaviour that is useful for REST servers:

* It can add CORS headers to response
* It handles `OPTIONS` requests and returns a response with CORS headers
  indicating which HTTP methods are supported.


Responding to requests
----------------------

A resource is only useful if it knows how to respond to HTTP requests. This
is done by adding methods and using the `view` decorator to inform the system
that they handle a specific HTTP method.

```python
@EventResource.GET()
def view(resource, request):
    return {...}


@EventResource.PUT()
def update(resource, request):
    return {...}
```

If a browser sends a `GET` request for `/events/12` an instance of the
`EventResource` class is created, and its `view` method is called to
generate a response.


Adding a controller
-------------------

A controller is a special type of resource which is used to trigger an action.
A controller is similar to a button: it does not have any state itself, but it
can modify state of something else. For example a reboot button which will
trigger a server reset. You can define a controller resource manually, but
you can also do so directly on a normal resource using the `controller`
decorator.


```python
@EventResource.controller(name='reboot')
def reboot(resource, request):
    return {...}
```

If you send a `POST` to `/servers/47/reboot` an instance of the `Server`
resource will be created, and its `reboot` method will be called.


Authorization
--------------

A resource acts as request context within Pyramid, so you can use Pyramid's
authorization framework directly. Just define a `__acl__` attribute or method
in your resource.

```python
from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid_rest import Resource


@resource(route_path='/events/{id:\d+}')
class EventResource(Resource):
    ...

    def __acl__(self):
        return [(Allow, Everyone, ['read']),
                (Allow, self.event.owner, ['delete', 'update'])]

@EventResource.GET(permission='read')
def view(self):
    return {...}
```


Design notes
============

- I opted to not include views inside the resource itself. The reasoning
  here is that 1) a view can be a class, and nested classes are not very
  readable, and 2) you can reuse a resource class in mulitple places
  by giving it multiple @resource decorators.

- There is deliberately no support for validation, default rendering or
  anything else. Since that can be very useful for users I can see adding
  that to the base package, but as very clear optional extras. For example
  by putting those in a pyramid_rest.ext.XYZ namespace.


Comparison to cornice
=====================

- Cornice has both a Service and a resource concept, but does not explain how
  they relate. Internally a resource creates a Service and adds views to it,
  but the rationale for the distinction is unclear. It mostly seems to be a
  design alternative: a Service has views as external functions or classes,
  while a resource is a class that is the resource and contains all its views
  as methods. resources also add extra magic collection-logic. All in all
  they seem like a vaguely defined convenience thing that should not be 
  (presented as) part of the core framework.

- Cornice does not seem to (conveniently) support a controller resource.

- I can't find any useful documentation for configurating ACLs or permissions
  with cornice. There is an `acl` parameters for the `Service` class, but
  that conflicts with `factory`. That seems like a strange un-pyramidy design.

- Cornice does a lot itself: filtering, validating, error handling, etc. A lot
  of that is unneeded for many REST services, and all of that can be added on
  top of a simpler framework, for example by using mix-in classes for resources.

- Cornice uses a global internally to track all registered resources. This makes
  it impossible to use multiple cornice instances in the same process (i.e. a
  composite app). Personally I find that a non-goal anyway, but it's arguably
  a design flaw.

- Interaction with standard Pyramid tools (predicates, request method filters,
  ACLs, etc. etc.) is either undocumented, very incompletely or missing
  completely.

- For completely unknown reasons cornice uses its own JSON renderer.
