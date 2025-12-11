// Marcar activo el menú según la página actual
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".sidebar a");
  const current = window.location.pathname.split("/").pop();
  links.forEach(link => {
    if (link.getAttribute("href") === current) {
      link.classList.add("active");
    }
  });

  // Simulación de acciones
  const aprobarBtns = document.querySelectorAll(".btn.aprobar");
  const rechazarBtns = document.querySelectorAll(".btn.rechazar");

  aprobarBtns.forEach(btn => {
    btn.addEventListener("click", () => alert("Solicitud aprobada "));
  });

  rechazarBtns.forEach(btn => {
    btn.addEventListener("click", () => alert("Solicitud rechazada "));
  });

  const deletes = document.querySelectorAll(".actions .delete");
  deletes.forEach(icon => {
    icon.addEventListener("click", () => alert("Cita eliminada "));
  });
});
