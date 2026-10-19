(function () {
  var STORAGE_KEY = "rs-cms-lang";
  // Суфікс — як у modeltranslation (id → ind, щоб не збігатися з FK-атрибутами <поле>_id).
  var LANG_CONFIG = [
    { code: "uk", suffix: "uk", label: "UA" },
    { code: "en", suffix: "en", label: "EN" },
    { code: "zh-hans", suffix: "zh_hans", label: "中文" },
    { code: "ms", suffix: "ms", label: "MS" },
    { code: "fil", suffix: "fil", label: "FIL" },
    { code: "id", suffix: "ind", label: "ID" },
    { code: "vi", suffix: "vi", label: "VI" }
  ];
  var LANGS = LANG_CONFIG.map(function (cfg) { return cfg.code; });

  function langConfig(code) {
    return LANG_CONFIG.filter(function (cfg) { return cfg.code === code; })[0] || LANG_CONFIG[0];
  }

  function langFromName(name) {
    if (!name) return "";
    for (var i = 0; i < LANG_CONFIG.length; i += 1) {
      var suffix = LANG_CONFIG[i].suffix;
      if (name.endsWith("_" + suffix) || name.indexOf("__text_html_" + suffix) !== -1) {
        return LANG_CONFIG[i].code;
      }
    }
    return "";
  }

  function fieldNameFromClass(el) {
    var cls = (el && el.className) || "";
    var m = String(cls).match(/(?:^|\s)(?:field|column)-([a-z0-9_]+)/i);
    return m ? m[1] : "";
  }

  function closestField(el) {
    // Unfold tabular: клітинка td, НЕ весь tr.form-row (інакше ховається весь рядок).
    var td = el.closest("td.field-tabular, td[class*='field-']");
    if (td) return td;
    return el.closest(".rs-cms-field")
      || el.closest(".form-row")
      || el.closest("[class*='field-']")
      || el.parentElement;
  }

  function markMatchingHeader(cell, lang, isOriginal) {
    if (!cell || cell.tagName !== "TD") return;
    var name = fieldNameFromClass(cell);
    if (!name) return;
    var table = cell.closest("table");
    if (!table) return;
    var th = table.querySelector("th.column-" + name);
    if (!th) return;
    if (isOriginal) {
      th.classList.add("rs-cms-original-alias");
    } else if (lang) {
      th.setAttribute("data-cms-lang", lang);
    }
  }

  function markFields() {
    document.querySelectorAll("[data-cms-lang]").forEach(function (el) {
      if (el.matches(".rs-cms-field, .form-row")) return;
      var wrap = closestField(el);
      if (wrap && !wrap.getAttribute("data-cms-lang")) {
        wrap.setAttribute("data-cms-lang", el.getAttribute("data-cms-lang"));
        markMatchingHeader(wrap, el.getAttribute("data-cms-lang"), false);
      }
    });

    document.querySelectorAll("input, textarea, select").forEach(function (el) {
      var lang = langFromName(el.getAttribute("name") || "");
      if (!lang) return;
      el.setAttribute("data-cms-lang", lang);
      var wrap = closestField(el);
      if (wrap) {
        wrap.setAttribute("data-cms-lang", lang);
        markMatchingHeader(wrap, lang, false);
      }
    });
  }

  function neutralizeOriginals() {
    document.querySelectorAll("input, textarea, select").forEach(function (el) {
      var name = el.getAttribute("name") || "";
      if (!name || langFromName(name) || el.type === "hidden" || el.type === "file") return;
      var hasTrans = LANGS.some(function (code) {
        return document.querySelector("[name='" + name + "_" + langConfig(code).suffix + "']");
      });
      if (!hasTrans) return;
      // readonly: значення йде в POST (disabled — ні, і виникає «тиха» помилка)
      el.readOnly = true;
      el.setAttribute("data-cms-original", "1");
      var wrap = closestField(el);
      // Ніколи не вішати на tr.form-row — у tabular це ховає весь рядок полів.
      if (wrap && wrap.tagName === "TR") {
        wrap = el.closest("td") || el.parentElement;
      }
      if (wrap) {
        wrap.classList.add("rs-cms-original-alias");
        markMatchingHeader(wrap, "", true);
      }
    });
  }

  function syncOriginalFromLang(lang) {
    if (LANGS.indexOf(lang) === -1) lang = "uk";
    var suffix = "_" + langConfig(lang).suffix;
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
      btn.textContent = langConfig(code).label;
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
    LANGS.forEach(function (code) { document.body.classList.remove("cms-lang-" + code); });
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
      var langHint = it.lang ? " [" + langConfig(it.lang).label + "]" : "";
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
    document.addEventListener("formset:added", function () {
      markFields();
      neutralizeOriginals();
      var lang = "uk";
      try {
        lang = localStorage.getItem(STORAGE_KEY) || "uk";
      } catch (err) {}
      applyLang(lang);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
