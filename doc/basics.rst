Basic usage
===========

Defining a resource
-------------------

.. code-block:: python

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

As you can see this the `resource` decorator is essentially a convenient way to
setup configure a route with a context factory. The `Resource` base class adds
some extra behaviour that is useful for REST servers:

* It can add CORS headers to response
* It handles ``OPTIONS`` requests and returns a response with CORS headers
  indicating which HTTP methods are supported.


Responding to requests
----------------------

A resource is only useful if it knows how to respond to HTTP requests. This
is done by adding methods and using the ``view`` decorator to inform the system
that they handle a specific HTTP method.

.. code-block:: python

   @EventResource.GET()
   def view(resource, request):
       return {...}
   
   
   @EventResource.PUT()
   def update(resource, request):
       return {...}

If a browser sends a ``GET`` request for ``/events/12`` an instance of the
``EventResource`` class is created, and its `view` method is called to
generate a response.


Adding a controller
-------------------

A controller is a special type of resource which is used to trigger an action.
A controller is similar to a button: it does not have any state itself, but it
can modify state of something else. For example a reboot button which will
trigger a server reset. You can define a controller resource manually, but
you can also do so directly on a normal resource using the `controller`
decorator.


.. code-block:: python

   @EventResource.controller(name='reboot')
   def reboot(resource, request):
       return {...}

If you send a ``POST`` to ``/servers/47/reboot`` an instance of the ``Server``
resource will be created, and its ``reboot`` method will be called.


Authorization
-------------

A resource acts as request context within Pyramid, so you can use Pyramid's
authorization framework directly. Just define a ``__acl__`` attribute or method
in your resource.

.. code-block:: python

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
