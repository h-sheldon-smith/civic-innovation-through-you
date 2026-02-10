(function () {
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(() => {
    const modal = document.getElementById("modal");
    const openBtn = document.getElementById("open-modal");
    const closeBtn = document.getElementById("close-modal");
    const closeBtn2 = document.getElementById("close-modal-2");

    // If the navbar/modal isn't on this page, do nothing
    if (!modal || !openBtn) return;

    function openModal() {
      modal.classList.add("is-open");
      modal.setAttribute("aria-hidden", "false");
    }

    function closeModal() {
      modal.classList.remove("is-open");
      modal.setAttribute("aria-hidden", "true");
    }

    openBtn.addEventListener("click", openModal);

    if (closeBtn) closeBtn.addEventListener("click", closeModal);
    if (closeBtn2) closeBtn2.addEventListener("click", closeModal);

    // Click outside the modal closes it
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeModal();
    });

    // ESC closes it
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeModal();
    });
  });
})();