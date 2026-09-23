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
      if (!name || langFromName(name) || el.type === "hidden" || el.type === "file") return;
      var hasTrans = LANGS.some(function (code) {
        var suffix = code === "zh-hans" ? "_zh_hans" : "_" + code;
        return document.querySelector("[name='" + name + suffix + "']");
      });
      if (!hasTrans) return;
      // readonly: значення йде в POST (disabled — ні, і виникає «тиха» помилка)
      el.readOnly = true;
      el.setAttribute("data-cms-original", "1");
      var wrap = el.closest(".form-row") || closestField(el);
      if (wrap) wrap.classList.add("rs-cms-original-alias");
    });
  }

  function syncOriginalFromLang(lang) {
    if (LANGS.indexOf(lang) === -1) lang = "uk";
    var suffix = lang === "zh-hans" ? "_zh_hans" : "_" + lang;
    document.querySelectorAll("[data-cms-original='1']").forEach(function (el) {
      var name = el.getAttribute("name") || "";
      if (!name) return;
      var trans = document.querySelector("[name='" + name + suffix + "']");
      if (!trans) return;
      var val = trans.value;
      if (window.tinymce) {
        var ed = tinymce.get(trans.id);
        if (ed) val = ed.getContent();
      }
      if (val) el.value = val;
    });
  }

  function prepareFormForSubmit() {
    var lang = "uk";
    try {
      lang = localStorage.getItem(STORAGE_KEY) || "uk";
    } catch (err) {}
    // Спочатку активна мова, потім UA як запасний варіант
    syncOriginalFromLang(lang);
    syncOriginalFromLang("uk");
    document.querySelectorAll("[data-cms-original='1']").forEach(function (el) {
      el.readOnly = false;
      el.disabled = false;
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

  function fieldLabel(wrap) {
    var lab = wrap && wrap.querySelector("label");
    if (lab && lab.textContent) return lab.textContent.replace(/\s*\*$/, "").trim();
    var cls = (wrap && wrap.className) || "";
    var m = cls.match(/field-([a-z0-9_]+)/i);
    return m ? m[1] : "Поле";
  }

  function revealErrors() {
    var items = [];
    document.querySelectorAll(".form-row, .rs-cms-field, [class*='field-']").forEach(function (wrap) {
      var list = wrap.querySelector(".errorlist, .errors, [data-error]");
      if (!list) return;
      var texts = [];
      list.querySelectorAll("li").forEach(function (li) {
        var t = (li.textContent || "").trim();
        if (t) texts.push(t);
      });
      if (!texts.length) {
        var raw = (list.textContent || "").trim();
        if (raw) texts.push(raw);
      }
      if (!texts.length) return;
      wrap.classList.add("has-cms-error");
      var lang = wrap.getAttribute("data-cms-lang") || "";
      items.push({
        label: fieldLabel(wrap),
        lang: lang,
        texts: texts,
      });
    });

    // non-field / form errors
    document.querySelectorAll(".messagelist .error, .errornote, ul.errorlist:not(.form-row ul)").forEach(function (el) {
      if (el.closest(".form-row, .rs-cms-field, [class*='field-']")) return;
      var t = (el.textContent || "").trim();
      if (t) items.push({ label: "Форма", lang: "", texts: [t] });
    });

    if (!items.length) return;

    var host = document.querySelector("#content .rs-cms-error-summary")
      || document.querySelector("#content-main .rs-cms-error-summary");
    if (!host) {
      host = document.createElement("div");
      host.className = "rs-cms-error-summary";
      host.setAttribute("role", "alert");
      var anchor = document.querySelector("#content-main") || document.querySelector("#content");
      if (anchor) anchor.insertBefore(host, anchor.firstChild);
    }
    var html = "<strong>Що виправити:</strong><ul>";
    items.forEach(function (it) {
      var langHint = it.lang ? " [" + (it.lang === "zh-hans" ? "中文" : it.lang.toUpperCase()) + "]" : "";
      html += "<li><span>" + it.label + langHint + ":</span> " + it.texts.join("; ") + "</li>";
    });
    html += "</ul>";
    host.innerHTML = html;

    // Показати мову першої помилки з іншої вкладки
    var firstLang = "";
    for (var i = 0; i < items.length; i++) {
      if (items[i].lang) {
        firstLang = items[i].lang;
        break;
      }
    }
    if (firstLang) applyLang(firstLang);
  }

  function bindSubmit() {
    document.querySelectorAll("#content-main form, form").forEach(function (form) {
      if (form.getAttribute("data-cms-submit-bound")) return;
      form.setAttribute("data-cms-submit-bound", "1");
      form.addEventListener("submit", function () {
        prepareFormForSubmit();
      });
    });
  }

  function init() {
    markFields();
    neutralizeOriginals();
    ensureToolbar();
    bindSubmit();
    var saved = "uk";
    try {
      saved = localStorage.getItem(STORAGE_KEY) || "uk";
    } catch (err) {}
    applyLang(saved);
    revealErrors();
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
