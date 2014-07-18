.. _philosophy-chapter:

Philosphy
=========

*rest_toolkit* tries to follow the standard
`REST <http://en.wikipedia.org/wiki/Representational_state_transfer>`_
standards for HTTP as much as possible:

* every URL uniquely identifies a *resource*
* an ``OPTIONS`` request must return the list of supported request methods in
  an ``Access-Control-Allow-Methods`` header.
* a request using an unsupported request method must return a HTTP 405 error.

A resource typically corresponds to something stored in a database. The mapping
does not need to be one-to-one: stored data can be exposed at multiple places
by an API, and each location is a separate resource from a REST point of view.
For example in an event management system a user can see see event information
in a list of events he has registered for as ``/users/12/events/13``, while an
event staff member manages the event via a ``/events/13``. Both URLs will use the
same event object in the database, but are separate REST resources, and will
return different data, use a different ACL, etc.

*rest_toolkit* follows this philosophy ant matches URLs to resources instead of
stored data. This has several advantages:

* your data model does not need to be aware of frontend-specific things like
  access control lists or JSON formatting.

* you can easily present the same data in multiple ways.

Request flow
------------

When processing a request pyramid will go through several steps.

.. graphviz::
   :alt: Visual overview of the request flow.

   digraph flow {
       rankdir=LR;
       node [shape=rounded, style=filled, penwidth=0.5, fontname=Arial, fontsize=12]
       edge [fontname="Arial:italic", fontsize=11, penwidth=0.5]

       request [label="GET /events/123"]
       resource [label="EventResource"]
       view [label="view_event() function"]
       response [label="JSON response"]

       request -> resource [label="Find resource\nfor /events/1"]
       resource -> view [label="Find GET view\nfor EventResource"]
       view -> response [label="Call view_event()"]
   }

1. When a request comes in the first step is to find a resource class which
   matches the requested URL.
2. The constructor for the resource class found in step 1 is called to create
   the resource instance. The constructor can raise an exception at this step
   to indicate no resource data could be found, for example if an requested
   id can not be found in a database.
3. Try to find a view for the resource and request type. This can either be a
   :ref:`default view <default-views>` or a view defined via an request method
   decorator. If no view is found a `HTTP 405 Method Not Allowed` error is
   returned.
4. The view is invoked. The data it returns will be converted to JSON and
   returned to the client.
