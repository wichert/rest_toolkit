angular.module("app", ['ngRoute', 'ngResource'])

  .value("endpointURL", "http://localhost:6543")

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
          todos: function ($route, Todos) {
            return Todos.get({}).$promise;
          }
        }
      })

      .when(
      '/todos/:todoId',
      {
        templateUrl: "view.partial.html",
        controller: "ViewCtrl",
        controllerAs: "ViewCtrl"
      })

      .when(
      '/todos/:todoId/edit',
      {
        templateUrl: "edit.partial.html",
        controller: "EditCtrl",
        controllerAs: "EditCtrl"
      })

      .otherwise({redirectTo: "/"})
  })

  .factory(
  "Todos",
  function ($resource) {
    return $resource(
      '/todos/:id',
      { id: '@id' },
      {
        update: {
          method: "PUT",
          isArray: false
        }
      });
  });