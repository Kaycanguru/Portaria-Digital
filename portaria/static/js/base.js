document.addEventListener("DOMContentLoaded", function () {

  // Mostrar/ocultar sidebar em dispositivos pequenos
  const sidebarToggle = document.getElementById("sidebarToggle");
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", function () {
      const sidebar = document.getElementById("sidebar");
      sidebar.classList.toggle("show");
    });
  }

  // Minimizar/maximizar sidebar em dispositivos maiores
  const sidebarMinimize = document.getElementById("sidebarMinimize");
  const logoImg = document.getElementById("logo-img");

  if (sidebarMinimize) {
    sidebarMinimize.addEventListener("click", function () {
      const sidebar = document.getElementById("sidebar");
      const spans = sidebar.querySelectorAll(".menu-text");
      const icon = this.querySelector("i");
      const topbar = document.getElementById("topbar"); // ← pega o navbar roxo

      if (sidebar.classList.contains("minimized")) {
        // Expandir sidebar
        sidebar.classList.remove("minimized");
        icon.classList.replace("bi-chevron-double-right", "bi-chevron-double-left");
        spans.forEach(span => span.style.display = "inline");
        if (logoImg) {
          logoImg.src = "/static/imagens/img-logo/horizontal-branca.jpg";
          logoImg.style.width = "10.5rem";
        }

        // Atualiza navbar roxa (topbar)
        if (topbar) {
          topbar.classList.remove("topbar-minimized");
          topbar.classList.add("topbar-full");
        }

      } else {
        // Minimizar sidebar
        sidebar.classList.add("minimized");
        icon.classList.replace("bi-chevron-double-left", "bi-chevron-double-right");
        spans.forEach(span => span.style.display = "none");
        if (logoImg) {
          logoImg.src = "/static/imagens/img-logo/ICONE-LOGO.jpg";
          logoImg.style.width = "3rem";
        }

        // Atualiza navbar roxa (topbar)
        if (topbar) {
          topbar.classList.remove("topbar-full");
          topbar.classList.add("topbar-minimized");
        }
      }

    });
  }
});

// Animação suave toda vez que a página é carregada.
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.fade-in').forEach(el => {
    el.classList.add('aparecer');
  });
});