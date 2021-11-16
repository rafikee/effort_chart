$(document).ready(function() {
  //reset the undo array
  localStorage.removeItem('actionsList')
  localStorage.removeItem('operationList')

  $(".stat-button").mousedown(function(event) {
    switch (event.which) {
      case 1:
        if ($('#addSub').text() == '+') {
          addsub(this, 1);
        }
        else {
          addsub(this, -1);
        }
        break;

      case 3:
        addsub(this, -1);
        break;
    }

    //Undo Logic
    var lastId = $(this).attr('id');
    a = '#' + lastId;
    var arr = JSON.parse(localStorage.getItem('actionsList'));
    var ops = JSON.parse(localStorage.getItem('operationList'));
    if (arr == null) {
      var arr = [];
    }
    if (ops == null) {
      var ops = [];
    }
    arr.push(a);
    ops.push($('#addSub').text());

    if (arr.length >= 10) {
      arr.shift();
    }
    if (ops.length >= 10) {
      ops.shift();
    }
    localStorage.setItem('actionsList',JSON.stringify(arr));
    localStorage.setItem('operationList',JSON.stringify(ops));
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

  $("#undo").mousedown(function(event) {
    var arr = JSON.parse(localStorage.getItem('actionsList'));
    var ops = JSON.parse(localStorage.getItem('operationList'));

    btn = arr[arr.length-1]
    op = ops[ops.length-1]

    if (op == '+') {
      addsub(btn, -1)
    }
    else {
      addsub(btn, 1)
    }
    arr.pop();
    ops.pop();
    localStorage.setItem('actionsList',JSON.stringify(arr));
    localStorage.setItem('operationList',JSON.stringify(ops));
  });

  // for editing the event name
  $("#idContentEditable").keypress(function(e){
    $.post($(location).attr('href'), {"myData": $(this).text()})
    return e.which != 13;
  });
});

function addsub(btn, numb) {
    var buttonText = $(btn).text();
    buttonText = parseInt(buttonText, 10) + numb;

    color = '#008000'; // green for +1
    if (numb < 0) color = '#FF0000'; // red for -1
    $(btn).css({
      backgroundColor: color
    });
    setTimeout(function() {
      $(btn).removeAttr('style');
    }, 250);
    $(btn).text(buttonText);
}
