(function () {
  var STORAGE_KEY = "rs-cms-lang";
  var LANGS = ["uk", "en", "zh-hans"];

  function langFromName(name) {
    if (!name) return "";
    if (name.endsWith("_zh_hans") || name.indexOf("__text_html_zh_hans") !== -1) return "zh-hans";
    if (name.endsWith("_uk") || name.indexOf("__text_html_uk") !== -1) return "uk";
    if (name.endsWith("_en") || name.indexOf("__text_html_en") !== -1) return "en";
    return "";
  }

  function closestField(el) {
    return el.closest(".rs-cms-field")
      || el.closest(".form-row")
      || el.closest("[class*='field-']")
      || el.parentElement;
  }

  function markFields() {
    document.querySelectorAll("[data-cms-lang]").forEach(function (el) {
      if (el.matches(".rs-cms-field, .form-row")) return;
      var wrap = closestField(el);
      if (wrap && !wrap.getAttribute("data-cms-lang")) {
        wrap.setAttribute("data-cms-lang", el.getAttribute("data-cms-lang"));
      }
    });

    document.querySelectorAll("input, textarea, select").forEach(function (el) {
      var lang = langFromName(el.getAttribute("name") || "");
      if (!lang) return;
      el.setAttribute("data-cms-lang", lang);
      var wrap = closestField(el);
      if (wrap) wrap.setAttribute("data-cms-lang", lang);
    });
  }

  function neutralizeOriginals() {
    document.querySelectorAll("input, textarea, select").forEach(function (el) {
      var name = el.getAttribute("name") || "";
      if (!name || langFromName(name) || el.type === "hidden") return;
      var hasTrans = LANGS.some(function (code) {
        var suffix = code === "zh-hans" ? "_zh_hans" : "_" + code;
        return document.querySelector("[name='" + name + suffix + "']");
      });
      if (!hasTrans) return;
      el.disabled = true;
      var wrap = el.closest(".form-row") || closestField(el);
      if (wrap) wrap.classList.add("rs-cms-original-alias");
    });
  }

  function ensureToolbar() {
    if (document.querySelector("[data-cms-langs]")) return;
    if (!document.querySelector("[data-cms-lang]")) return;
    var bar = document.createElement("div");
    bar.className = "rs-cms-langs";
    bar.setAttribute("data-cms-langs", "");
    bar.setAttribute("role", "tablist");
    bar.setAttribute("aria-label", "Мова полів");
    LANGS.forEach(function (code) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "rs-cms-langs__btn";
      btn.setAttribute("data-cms-lang-btn", code);
      btn.setAttribute("role", "tab");
      btn.textContent = code === "zh-hans" ? "中文" : code === "en" ? "EN" : "UA";
      bar.appendChild(btn);
    });
    var cms = document.querySelector(".rs-cms");
    if (cms) {
      var head = cms.querySelector(".rs-cms__head");
      if (head) head.insertAdjacentElement("afterend", bar);
      else cms.insertBefore(bar, cms.firstChild);
      return;
    }
    var content = document.querySelector("#content");
    if (content) {
      content.insertBefore(bar, content.firstChild);
      return;
    }
    var form = document.querySelector("#content-main form, form");
    if (form && form.parentNode) form.parentNode.insertBefore(bar, form);
  }

  function applyLang(lang) {
    if (LANGS.indexOf(lang) === -1) lang = "uk";
    document.body.classList.remove("cms-lang-uk", "cms-lang-en", "cms-lang-zh-hans");
    document.body.classList.add("cms-lang-" + lang);
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (err) {}
    document.querySelectorAll("[data-cms-lang-btn]").forEach(function (btn) {
      var on = btn.getAttribute("data-cms-lang-btn") === lang;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });
    if (window.tinymce && tinymce.editors) {
      window.setTimeout(function () {
        tinymce.editors.forEach(function (ed) {
          try {
            ed.fire("ResizeEditor");
          } catch (err) {}
        });
      }, 40);
    }
  }

  function init() {
    markFields();
    neutralizeOriginals();
    ensureToolbar();
    var saved = "uk";
    try {
      saved = localStorage.getItem(STORAGE_KEY) || "uk";
    } catch (err) {}
    applyLang(saved);
    document.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-cms-lang-btn]");
      if (!btn) return;
      event.preventDefault();
      applyLang(btn.getAttribute("data-cms-lang-btn"));
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
