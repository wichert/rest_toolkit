Changelog
=========

0.6 - November 4, 2014
----------------------

- Make sure controllers for resource whose path do not end in a slash are
  reachable.  This fixes `issue 12
  <https://github.com/wichert/rest_toolkit/issues/12>`_.

- Fix mismatch between code and documentation: use ``request_method``
  as parameter name for the ``controller`` decorator.


0.5 - October 24, 2014
----------------------

- Allow overriding the request method for controllers. This fixes
  `issue 10 <https://github.com/wichert/rest_toolkit/issues/10>`_.

- Add ``read_permission``, ``update_permission`` and ``delete_permission``
  options to the ``resource`` decorator to set permissions for default views.
  This fixes `issue 8 <https://github.com/wichert/rest_toolkit/issues/8>`_.

- Rely on fixtures provided by pyramid_sqlalchemy for our SQL-related tests.

- Preserve headers when converting a HTTP response to JSON. This fixes
  `issue 6 <https://github.com/wichert/rest_toolkit/issues/6>`_.

- The route name for a resource can now be configured with a ``route_name`` parameter
  for the ``resource`` decorator.


0.4.1 - July 18, 2014
---------------------

- Make sure all raised HTTP exceptions are converted to JSON responses.


0.4 - July 18, 2014
-------------------

This releases focuses on improving the documentation and fixing problems in the
SQL extension.

- Fix several errors in the SQLResource defaults views.

- Configuring the SQL extension is no longer necessary if you use
  `pyramid_sqlalchemy <https://pyramid-sqlalchemy.readthedocs.org>`_ to handle
  SQLAlchemy integration.

- `Travis <https://travis-ci.org/wichert/pyramid_sqlalchemy>`_ is now setup to
  automatically run tests on CPython 2.7, CPython 3.3, CPython 3.4 and PyPy.

- Fix Python 3 compatibility problem in the generic error view.

- Drop explicit Python 2.6 support. The tests use too many set literals to make
  Python 2.6 worthwile.

- Modify EditableResource to not inherit from ViewableResource. This makes
  the separation between editing and viewing explicit, and works around the
  inability of Python to handle the inheritance schemes where a base classes 
  is used multiple times.

- Remove the default value for ``replace`` in
  ``EditableResource.updat_from_dict()``. This did not serve a useful purpose,
  and could be confusing.

- Set ``self.request`` in SQLResource constructor.


0.3 - July 11, 2014
-------------------

This release fixes several critical errors in the SQL extension:

- Fix the invoction of the context query.

- Return not-found error from SQLResource instead of an internal error when no
  SQL row could be found.

- Do not enable default views for SQLResource automatically. This should be
  an explicit decision by the user.


0.2.2 - July 11, 2014
---------------------

- Fix several errors in SQL extension.


0.2.1 - July 10, 2014
---------------------

- Add a MANIFEST.in to the source distribution installable.


0.2 - July 9, 2014
------------------

- Several demos showing how to use rest_toolkit with AngularJS have been added.

- Support for default DELETE, GET, PATCH and PUT views has been added.

- Various documentation fixes and improvements.


0.1 - Released 24 June, 2014
----------------------------

This is the first release.
