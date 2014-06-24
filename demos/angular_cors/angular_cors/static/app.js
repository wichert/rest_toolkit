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

      .when(
      '/todos/:todoId/edit',
      {
        templateUrl: "/static/edit.partial.html",
        controller: "EditCtrl",
        controllerAs: "EditCtrl"
      })

      .otherwise({redirectTo: "/"})
  })

  .controller(
  "ListCtrl",
  function ($http) {
    var ctrl = this;
    ctrl.todos = [];
    ctrl.newTitle = "";

    $http.get("/todos")
      .success(function (data) {
                 ctrl.todos = data.todos;
               });

    ctrl.addTodo = function (todoTitle) {
      $http.post("/todos", {title: todoTitle})
        .success(function (data) {
                   ctrl.todos.push(data.todo);
                   ctrl.newTitle = "";
                 });
    };

    ctrl.deleteTodo = function (todoId) {
      $http.delete("/todos/" + todoId)
        .success(function () {
                   // Removed on the server, let's remove locally
                   _.remove(ctrl.todos, {id: todoId});
                 });
    };

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
  })

  .controller(
  "EditCtrl",
  function ($routeParams, $http, $location) {
    var ctrl = this;
    var todoId = $routeParams.todoId;

    ctrl.todo = {};
    $http.get("/todos/" + todoId)
      .success(function (data) {
                 ctrl.todo.title = data.title;
               });

    // Handle the submit
    ctrl.updateTodo = function () {
      $http.put("/todos/" + todoId, ctrl.todo)
        .success(function () {
                   $location.path("#/");
                 });
    }
  });