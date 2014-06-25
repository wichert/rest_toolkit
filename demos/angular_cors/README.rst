===================
angular_cors README
===================

Running the AngularJS frontend at a different URL than the backend.

Shows
=====

- Starts with ``demos/angular/resource``

- Wires up the Pyramid ``Configurator`` to allow cross-origin requests

Usage
=====

- ``python app.py``

- Go to ``static/index.html`` on your local webserver outside Pyramid

Implementation
==============

- Instead of using ``quick_serve``, wire up a Pyramid application
  using the configurator

- Extend the configuration using events that put the CORS information
  on responses