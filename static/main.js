$(document).ready(function() {

  $(".stat-button").mousedown(function(event) {
    var buttonText = $(this).text();
    switch (event.which) {
      case 1:
        buttonText = parseInt(buttonText, 10) + 1;
        $(this).css({backgroundColor: '#008000'});
        break;
      case 3:
        buttonText = parseInt(buttonText, 10) - 1;
        $(this).css({backgroundColor: '#FF0000'});
        break;
    }
    var that = this;
    setTimeout(function(){
      $(that).removeAttr('style');
    }, 250);
    $(this).text(buttonText);
  });

  $(".stat-button").bind("contextmenu", function(e) {
    return false;
  });

  $(".stat-button").on("taphold",function(){
    var buttonText = $(this).text();
    buttonText = parseInt(buttonText, 10) - 1;
    $(this).css({backgroundColor: '#FF0000'});
    var that = this;
    setTimeout(function(){
      $(that).removeAttr('style');
    }, 250);
    $(this).text(buttonText);
  });

});
