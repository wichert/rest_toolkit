=========================
angular_helloworld README
=========================

A tiny Todo example of an AngularJS app fronting a simple endpoint.

Shows
=====

- A static HTML page with AngularJS providing the UI

- A REST endpoint that provides a list of Todo items

Usage
=====

- ``python app.py``

- Go to ``http://localhost:8088/static/index.html``

Implementation
==============

- Pyramid-based Python server providing a ``rest_toolkit`` endpoint and 
  serving up static files like an HTTP server
  
- Uses the demo-oriented ``quick_serve`` from ``rest_toolkit`` to point 
  at the static files and serve them up under 
  ``http://localhost:8088/static`` with the REST API under 
  ``http://localhost:8088/todos``
  
- An AngularJS application in ``index.html`` which loads the module in 
  ``app.js``, plus Boostrap CSS