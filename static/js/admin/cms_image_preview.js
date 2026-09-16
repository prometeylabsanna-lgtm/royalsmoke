(function () {
  function bindInput(input) {
    if (input.dataset.cmsImageBound) return;
    input.dataset.cmsImageBound = "1";
    input.addEventListener("change", function () {
      var file = input.files && input.files[0];
      var wrap = input.closest("[data-cms-image]") || input.closest(".form-row") || input.parentElement;
      if (!wrap) return;
      var frame = wrap.querySelector(".rs-cms-image__frame");
      var img = wrap.querySelector("[data-cms-image-preview]");
      var placeholder = wrap.querySelector("[data-cms-image-placeholder]");
      if (!img) {
        img = document.createElement("img");
        img.className = "rs-cms-image__preview";
        img.setAttribute("data-cms-image-preview", "");
        img.alt = "";
        if (frame) {
          frame.insertBefore(img, frame.firstChild);
        } else {
          wrap.insertBefore(img, wrap.firstChild);
        }
      }
      var clearBox = wrap.querySelector("[data-cms-image-clear]");
      if (!file) return;
      if (file.type && file.type.indexOf("image/") !== 0) return;
      if (img.dataset.objectUrl) {
        URL.revokeObjectURL(img.dataset.objectUrl);
      }
      var url = URL.createObjectURL(file);
      img.dataset.objectUrl = url;
      img.src = url;
      img.hidden = false;
      img.classList.remove("is-empty");
      if (frame) frame.classList.remove("is-empty");
      if (placeholder) placeholder.hidden = true;
      if (clearBox) clearBox.checked = false;
    });
  }

  function bindClear(box) {
    if (box.dataset.cmsImageClearBound) return;
    box.dataset.cmsImageClearBound = "1";
    box.addEventListener("change", function () {
      var wrap = box.closest("[data-cms-image]") || box.closest(".form-row");
      if (!wrap) return;
      var frame = wrap.querySelector(".rs-cms-image__frame");
      var img = wrap.querySelector("[data-cms-image-preview]");
      var placeholder = wrap.querySelector("[data-cms-image-placeholder]");
      if (!img) return;
      img.hidden = box.checked;
      if (frame) {
        frame.classList.toggle("is-empty", box.checked);
      }
      if (placeholder) {
        placeholder.hidden = !box.checked;
      }
    });
  }

  function init() {
    document.querySelectorAll("input[type=file][accept='image/*'], [data-cms-image-input]").forEach(bindInput);
    document.querySelectorAll("[data-cms-image-clear]").forEach(bindClear);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
