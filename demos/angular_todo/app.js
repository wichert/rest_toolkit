angular.module("app", ['ngRoute'])

  .value("endpointURL", "http://localhost:8088")

  .config(
  function ($routeProvider) {

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
  })

  .controller(
  "ListCtrl",
  function ($http, endpointURL) {
    var ctrl = this;
    ctrl.todos = [];
    ctrl.newTitle = "";

    $http.get(endpointURL + "/todos")
      .success(function (data) {
                 ctrl.todos = data.todos;
               });

    ctrl.addTodo = function (todoTitle) {
      $http.post(endpointURL + "/todos", {title: todoTitle})
        .success(function (data) {
                   ctrl.todos.push(data.todo);
                   ctrl.newTitle = "";
                 });
    };

    ctrl.deleteTodo = function (todoId) {
      $http.delete(endpointURL + "/todos/" + todoId)
        .success(function () {
                   // Removed on the server, let's remove locally
                   _.remove(ctrl.todos, {id: todoId});
                 });
    };

  })

  .controller(
  "ViewCtrl",
  function ($routeParams, $http, endpointURL) {
    var ctrl = this;
    var todoId = $routeParams.todoId;

    ctrl.todo = {};
    $http.get(endpointURL + "/todos/" + todoId)
      .success(function (data) {
                 ctrl.todo = data;
               });
  })

  .controller(
  "EditCtrl",
  function ($routeParams, $http, $location, endpointURL) {
    var ctrl = this;
    var todoId = $routeParams.todoId;

    ctrl.todo = {};
    $http.get(endpointURL + "/todos/" + todoId)
      .success(function (data) {
                 ctrl.todo.title = data.title;
               });

    // Handle the submit
    ctrl.updateTodo = function () {
      $http.put(endpointURL + "/todos/" + todoId, ctrl.todo)
        .success(function () {
                   $location.path("#/");
                 });
    }
  });