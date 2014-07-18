*rest_toolkit* is a Python package which provides a very convenient way to
build REST servers. It is build on top of
`Pyramid <http://www.pylonsproject.org/projects/pyramid/about>`_, but you do not
need to know much about Pyramid to use rest_toolkit.


Quick example
=============

This is a minimal example which defines a ``Root`` resource with a ``GET``
view, and starts a simple HTTP server. If you run this example you can request
``http://localhost:8080/`` and you will see a JSON response with a status
message.

::

   from rest_toolkit import quick_serve
   from rest_toolkit import resource


   @resource('/')
   class Root(object):
       def __init__(self, request):
           pass


   @Root.GET()
   def show_root(root, request):
       return {'status': 'OK'}


   if __name__ == '__main__':
       quick_serve()
