$(document).ready(function() {
  $(".stat-button").mousedown(function(event) {
    var buttonText = $(this).text();
    switch (event.which) {
      case 1:
        buttonText = parseInt(buttonText, 10) + 1;
        break;
      case 3:
        buttonText = parseInt(buttonText, 10) - 1;
        break;
    }
    $(this).text(buttonText);
  });
  $(".stat-button").bind("contextmenu", function(e) {
    return false;
  });
});
