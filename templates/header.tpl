<!DOCTYPE html>
<head>
<base href="/template">
<link rel="stylesheet" type="text/css" href="css/temp.css">
<!-- load jquery and global js scripts -->
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script src="js/script_head.js"></script>
<!-- <script src="js/script_encryption.js"></script> -->

<title>NoThreeDots</title>
</head>

<div class="header-menu-section">
  <h1 id="title" onclick="goto()" onmouseover="showText(150)" onmouseout="rmtext(150)">NoThreeDots</h1>
  <ul id="header-menu">
  </ul>
</div>
<script src="js/header.js"></script>

<script>
  function goto() {
    if (window.sessionStorage.getItem("loggedIn") === "True") {
      document.location.href = "/home"
    } else {
      document.location.href = "/"
    }
  }

function add() {
  document.getElementById("title").innerHTML = document.getElementById("title").innerHTML + ".";
}

function rm() {
  if (document.getElementById("title").innerHTML.length > 11) {
    document.getElementById("title").innerHTML = document.getElementById("title").innerHTML.slice(0, -1);
  }
}

var showText = function (interval) {
  for (var i = 1; i < 4; i++) {
    setTimeout(add, interval * i);
  }
}

var rmtext = function (delay) {   
  for (var i = 1; i < 4; i++) {
    setTimeout(rm, delay * i);
  }
}
</script>
