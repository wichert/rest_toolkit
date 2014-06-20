Security
========

*rest_toolkit* allows you to use the :ref:`Pyramid's security
<pyramid:security-chapter>` system directly. To use this you need to do a
couple of things:

* :ref:`Configure authentication and authorization policies
  <pyramid:enabling-authorization-policy>`.
* Define an :ref:`Access Control List (ACL) <pyramid:elements-of-an-acl>` for
  your resources.


Since REST resources as request context (sometimes also called request
objects in Pyramid's documentation) protection resources is as simple as
adding an ``__acl__`` attribute or method to your resource, and specifying a
permission on a view.


.. code-block:: python
   :linenos:
   :emphasize-lines: 10,11,12,14

   from pyramid.security import Allow
   from pyramid.security import Everyone
   from pyramid_rest import Resource
   
   
   @resource(route_path='/events/{id:\d+}')
   class EventResource(Resource):
       ...
   
       def __acl__(self):
           return [(Allow, Everyone, ['read']),
                   (Allow, self.event.owner.id, ['delete', 'update'])]
   
   @EventResource.GET(permission='read')
   def view(self):
       return {...}


This example above uses a method to define the ACL in lines 10-12. The ACL does
two things: it specifies that everyone has `read`-permissions, and the owner
of the event also has `delete` and `update` permissions. The ``GET`` view
is the configured to require the read-permission in line 14.