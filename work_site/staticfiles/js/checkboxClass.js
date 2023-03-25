function myFunction() {
  var cb = document.getElementById('checkAll');
  var logo = document.getElementByTagName('tr');

  if (cb.checked) {
    logo.setAttribute("class", "color");
  } else {
    logo.removeAttribute("class");
  }
}