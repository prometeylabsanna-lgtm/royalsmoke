/**
 * Картка товару: блок «Фото товару» над fieldset «Відео».
 */
(function () {
  function findPhotos() {
    return (
      document.getElementById("productimage_set-group") ||
      document.querySelector(".inline-group.rs-product-images-inline")
    );
  }

  function findVideoAnchor() {
    var videoInput =
      document.querySelector(".field-video_file") ||
      document.querySelector("[name='video_file']");
    if (!videoInput) return null;

    var node = videoInput.closest("fieldset") || videoInput.closest("[class*='fieldset']");
    if (!node) {
      var row = videoInput.closest(".form-row") || videoInput.parentElement;
      node = row && row.parentElement;
    }
    if (!node) return null;

    // Підняти до сусіда інлайнів (спільний батько), щоб insertBefore спрацював
    var photos = findPhotos();
    if (!photos) return node;
    while (node.parentElement && !node.parentElement.contains(photos)) {
      node = node.parentElement;
    }
    while (
      node.parentElement &&
      node.parentElement.contains(photos) &&
      node.parentElement !== photos.parentElement
    ) {
      node = node.parentElement;
    }
    return node;
  }

  function placePhotosAboveVideo() {
    var photos = findPhotos();
    var video = findVideoAnchor();
    if (!photos || !video || !video.parentNode) return;
    if (photos === video) return;
    if (
      photos.compareDocumentPosition(video) & Node.DOCUMENT_POSITION_FOLLOWING &&
      photos.parentNode === video.parentNode
    ) {
      return;
    }
    video.parentNode.insertBefore(photos, video);
  }

  function run() {
    placePhotosAboveVideo();
    window.setTimeout(placePhotosAboveVideo, 50);
    window.setTimeout(placePhotosAboveVideo, 250);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
