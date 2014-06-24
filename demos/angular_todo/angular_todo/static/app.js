angular.module("app", ['ngRoute'])

  .config(
  function ($routeProvider) {

    $routeProvider
      .when(
      '/',
      {
        templateUrl: "/static/list.partial.html",
        controller: "ListCtrl",
        controllerAs: "ListCtrl"
      })

      .when(
      '/todos/:todoId',
      {
        templateUrl: "/static/view.partial.html",
        controller: "ViewCtrl",
        controllerAs: "ViewCtrl"
      })

      .otherwise({redirectTo: "/"})
  })

  .controller(
  "ListCtrl",
  function ($http) {
    var ctrl = this;
    ctrl.todos = [];
    $http.get("/todos")
      .success(function (data) {
                 ctrl.todos = data.todos;
               });
  })

  .controller(
  "ViewCtrl",
  function ($routeParams, $http) {
    var ctrl = this;
    var todoId = $routeParams.todoId;

    ctrl.todo = {};
    $http.get("/todos/" + todoId)
      .success(function (data) {
                 ctrl.todo = data;
               });
  });