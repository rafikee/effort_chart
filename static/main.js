$(document).ready(function() {

  $(".stat-button").mousedown(function(event) {

    var numb = 1;
    var background = '#008000';
    var operation = $('#addSub').text();
    if (operation != '+') {
      var numb = -1;
      var background = '#FF0000';
    }

    var buttonText = $(this).text();
    switch (event.which) {
      case 1:
        buttonText = parseInt(buttonText, 10) + numb;
        $(this).css({
          backgroundColor: background
        });
        break;

      case 3:
        buttonText = parseInt(buttonText, 10) - 1;
        $(this).css({
          backgroundColor: '#FF0000'
        });
        break;
    }
    var that = this;
    setTimeout(function() {
      $(that).removeAttr('style');
    }, 250);
    $(this).text(buttonText);

    //begin logic for undo, store these in an array
    lastId = $(this).attr('id');
    //console.log($('#' + lastId));
  });

  $(".stat-button").bind("contextmenu", function(e) {
    return false;
  });

  $("#addSub").mousedown(function(event) {
    var currentText = $(this).text();
    if (currentText == '+') {
      $(this).text("-");
      $(this).css({
        backgroundColor: 'red'
      });
    }
    else {
      $(this).text("+");
      $(this).css({
        backgroundColor: 'green'
      });
    }
  });

});
