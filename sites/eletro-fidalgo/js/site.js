(function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (header && toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var form = document.querySelector("#contato-form");
  var status = document.querySelector("#form-status");
  if (form && status) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      status.classList.add("is-visible");
      status.focus();
    });
  }
})();
