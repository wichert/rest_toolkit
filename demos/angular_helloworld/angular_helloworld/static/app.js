angular.module("app", [])

  .controller("HomeCtrl", function ($http) {
                var ctrl = this;
                ctrl.todos = [];
                $http.get("/todos")
                  .success(function (data) {
                             ctrl.todos = data.todos;
                           });
              });