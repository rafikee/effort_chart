$(document).ready(function() {

  $(".stat-button").mousedown(function(event) {
    var buttonText = $(this).text();
    switch (event.which) {
      case 1:
        buttonText = parseInt(buttonText, 10) + 1;
        $("#plus").fadeIn();
        $("#plus").fadeOut();
        break;
      case 3:
        buttonText = parseInt(buttonText, 10) - 1;
        $("#minus").fadeIn();
        $("#minus").fadeOut();
        break;
    }
    $(this).text(buttonText);
  });

  $(".stat-button").bind("contextmenu", function(e) {
    return false;
  });

  $(".stat-button").on("taphold",function(){
    var buttonText = $(this).text();
    buttonText = parseInt(buttonText, 10) - 1;
    $(this).text(buttonText);
    $("#minus").fadeIn();
    $("#minus").fadeOut();
  });

});
