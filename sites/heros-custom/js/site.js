(function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (header && toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var WA = "https://wa.me/5541991878091";
  var MAIL = "heroscustomeletric@gmail.com";

  var SERVICO_LABEL = {
    "visita-institucional": "Visita institucional",
    "vistoria-passaporte": "Vistoria / Passaporte Digital",
    "preventiva-corretiva": "Preventiva / corretiva",
    "clube-guarda": "Clube / guarda",
    "vaga-curadoria": "Vaga de curadoria",
  };

  function readServicoParam() {
    try {
      return new URLSearchParams(window.location.search).get("servico") || "";
    } catch (err) {
      return "";
    }
  }

  function applyServico(value) {
    var select = document.querySelector("#servico");
    if (!select || !value) return;
    if (SERVICO_LABEL[value] || select.querySelector('option[value="' + value + '"]')) {
      select.value = value;
    }
  }

  applyServico(readServicoParam());

  document.querySelectorAll("[data-servico]").forEach(function (el) {
    el.addEventListener("click", function () {
      applyServico(el.getAttribute("data-servico"));
    });
  });

  function fieldValue(form, name) {
    var field = form.elements.namedItem(name);
    return field && typeof field.value === "string" ? field.value.trim() : "";
  }

  function buildMessage(form) {
    var servico = fieldValue(form, "servico");
    var linhas = [
      "Heros Custom — interesse (rascunho MVP, sem checkout)",
      "Nome: " + fieldValue(form, "nome"),
      "WhatsApp: " + fieldValue(form, "telefone"),
      "Veículo: " + fieldValue(form, "veiculo"),
      "Serviço: " + (SERVICO_LABEL[servico] || servico),
      "Observações: " + (fieldValue(form, "notas") || "—"),
    ];
    return linhas.join("\n");
  }

  function openWhatsApp(text) {
    window.location.href = WA + "?text=" + encodeURIComponent(text);
  }

  function openMailto(text, servico) {
    var label = SERVICO_LABEL[servico] || servico || "interesse";
    var subject = "Heros Custom — " + label;
    window.location.href = "mailto:" + MAIL +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(text);
  }

  var form = document.querySelector("#contato-form");
  var status = document.querySelector("#form-status");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (typeof form.reportValidity === "function" && !form.reportValidity()) {
        return;
      }
      var channel = (event.submitter && event.submitter.getAttribute("data-channel")) || "whatsapp";
      var text = buildMessage(form);
      if (status) {
        status.textContent = channel === "mailto"
          ? "Abrindo o cliente de e-mail com o texto pronto. Se nada abrir, use heroscustomeletric@gmail.com."
          : "Abrindo o WhatsApp da oficina com o texto pronto. Se nada abrir, use (41) 99187-8091.";
        status.classList.add("is-visible");
      }
      if (channel === "mailto") {
        openMailto(text, fieldValue(form, "servico"));
      } else {
        openWhatsApp(text);
      }
    });
  }
})();
