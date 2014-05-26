Resource types
--------------

Three types of resources:

1. Element: a single entity, for example a user.
2. Collection: a collection of entities, for example the list of all known users.
3. Controller: a source which only performs some action. Typically a controller
   only response to a `POST` request.

A resource typically corresponds to something stored in a database. The mapping
does not need to be one-to-one: stored data can be exposed at multiple places
by an API, and each location is a separate resource from a REST point of view.
For example in an event management system a user can see see event information
in a list of events he has registered for as `/users/12/events/13`, while an
event staff member manages the event via a `/events/13`. Both URLs will use the
same event object in the database, but are separate REST resources, and will
return different data, use a different ACL, etc.


Defining a resource
-------------------

```python
from pyramid_rest import Resource
from .models import DBSession
from .models import Event


@resource(route_path='/events/{id:\d+}')
class EventResource(Resource):
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
