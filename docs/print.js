// Expand all <details> elements before printing so handouts print in full
window.addEventListener('beforeprint', function () {
  document.querySelectorAll('details').forEach(function (el) {
    el.setAttribute('open', '');
  });
});
