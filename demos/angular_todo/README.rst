===================
angular_todo README
===================

CRUD Todo example using AngularJS in a single-page application (SPA).

Shows
=====

- List/Add/View/Edit/Delete on Todo items

- Single-page application with views for list/edit/view

Usage
=====

- ``python app.py``

- Go to ``http://localhost:8088/static/index.html``

Implementation
==============

- Angular routes in ``app.py`` which provides the template/controller
  for each view, plus resolves any needed promises for getting data
  before opening the view

- Collection and Item resources in ``app.py`` with a module-level
  dictionary holding the (modifiable) listing of todo items
