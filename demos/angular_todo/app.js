angular.module("app", ['ngRoute'])

  .value("endpointURL", "http://localhost:8088")

  .config(function ($routeProvider) {

            $routeProvider
              .when(
              '/',
              {
                templateUrl: "list.partial.html",
                controller: "ListCtrl",
                controllerAs: "ListCtrl"
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
          });