document.getElementById('link-with-redirect').addEventListener('click', function() {
  setTimeout(function() {
    // Should be triggered after download started
    document.location.href='{% url "myapp:table" %}';
  });
 }, false);