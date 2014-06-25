=======================
angular_resource README
=======================

CRUD Todo example using AngularJS's ``$resource`` abstraction for
REST APIs.

Shows
=====

- List/Add/View/Edit/Delete on Todo items via an ngResource factory

Usage
=====

- ``python app.py``

- Go to ``http://localhost:6543/``

Implementation
==============

- Uses ``demos/angular_todo`` as the starting point

- Replaces ``$http`` with ``$resource``

- This reduces the amount of code significantly

- It also shows the conventional pattern for design of the URL space
  client-side and server-side