angular.module("app", ['ngRoute', 'ngResource'])

  .value("endpointURL", "http://localhost:8088")

  .config(
  function ($routeProvider) {

    $routeProvider
      .when(
      '/',
      {
        templateUrl: "list.partial.html",
        controller: "ListCtrl",
        controllerAs: "ListCtrl",
        resolve: {
          todoList: function (Todos) {
            return Todos.get({}).$promise;
          }
        }
      })

      .when(
      '/todos/:todoId',
      {
        templateUrl: "view.partial.html",
        controller: "ViewCtrl",
        controllerAs: "ViewCtrl",
        resolve: {
          todo: function (Todos, $route) {
            return Todos
              .get({id: $route.current.params.todoId}).$promise;
          }
        }
      })

      .when(
      '/todos/:todoId/edit',
      {
        templateUrl: "edit.partial.html",
        controller: "EditCtrl",
        controllerAs: "EditCtrl",
        resolve: {
          todo: function (Todos, $route) {
            return Todos
              .get({id: $route.current.params.todoId}).$promise;
          }
        }
      })

      .otherwise({redirectTo: "/"})
  })

  .factory(
  "Todos",
  function ($resource, endpointURL) {
    return $resource(
        endpointURL + '/todos/:id',
        { id: '@id' },
        {
          update: {
            method: "PUT",
            isArray: false
          }
        });
  });