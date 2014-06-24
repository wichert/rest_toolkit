angular.module("app")

  .controller(
  "ListCtrl",
  function ($http, Todos, todoList) {

    var ctrl = this;
    ctrl.todos = todoList.data;
    ctrl.newTitle = "";

    ctrl.addTodo = function (todoTitle) {
      Todos
        .save({}, {title: todoTitle},
              function (todo) {
                ctrl.todos.push(todo.data);
                ctrl.newTitle = "";
              }
      );
    };

    ctrl.deleteTodo = function (todoId) {
      Todos
        .delete({id: todoId}, function () {
                  // Removed on the server, let's remove locally
                  _.remove(ctrl.todos, {id: todoId});
                });
    };

  })


  .controller("ViewCtrl", function (todo) {
                this.todo = todo;
              })


  .controller(
  "EditCtrl",
  function (todo, $location, endpointURL) {
    var ctrl = this;
    ctrl.todo = todo;

    // Handle the submit
    ctrl.updateTodo = function () {
      todo.$update(function () {
        $location.path(endpointURL);
      });
    }
  });