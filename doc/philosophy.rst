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

