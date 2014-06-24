angular.module("app")

  .controller(
  "ListCtrl",
  function ($log, $http, endpointURL, todos) {

    var ctrl = this;
    ctrl.todos = todos.data;
    ctrl.newTitle = "";

    ctrl.addTodo = function (todoTitle) {
      $http.post(endpointURL + "/todos", {title: todoTitle})
        .success(function (todo) {
                   ctrl.todos.push(todo.data);
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