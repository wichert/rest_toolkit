angular.module("app", [])

  .value("endpointURL", "http://localhost:8088")

  .controller("HomeCtrl", function ($http, endpointURL) {
                var ctrl = this;
                ctrl.todos = [];
                $http.get(endpointURL + "/todos")
                  .success(function (data) {
                             ctrl.todos = data.todos;
                           });
              });