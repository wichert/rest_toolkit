Comparison with other frameworks
================================

cornice
-------

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

- For unknown reasons cornice uses its own JSON renderer.

- cornice has some facilities to automatically create documentation for an
  API using code comments and colander schemas. rest_toolkit does not try to
  do that: in my experience good documentation can never be generated.
  Writing documentation requires a different mindset and structure than
  writing code, and you should not try to mix the two.



Django REST
-----------

- A Django app, which means have to use Django infrastructure and
  tools. This may not be a good match for non-typical Django applications.

- It implements its own authorisation mechanism. I’m guessing Django does not
  have a standard version it can leverage?

- Require a bit more boilerplate than should be necessary.


sandman
-------

- sandman forces your REST API structure to exactly match your database model.
  In non-trivial systems that will generally not work: if there is any
  hierarchy in your data model sandman will not reflect that, normalisation is
  not undone in a REST API which means your REST interface will be much more
  complex and require more requests than needed, relationships between objects
  are not exposed.

- sandman does not support any form of authorisation. You can either do nothing
  at all, or everything.

- sandman does not support any way to add controllers that perform actions.
  Since it’s flask under the hook you could probably add that yourself if
  necessary, but this is undocumented.

