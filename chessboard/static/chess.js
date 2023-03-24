function move(){
  var src = document.getElementById("src").value;
  var dst = document.getElementById("dst").value;
  var piece = document.getElementById(src).innerHTML;
  document.getElementById(dst).innerHTML = piece;
  document.getElementById(src).innerHTML = "&nbsp";
}

function reset(){
  window.location.reload();
}
