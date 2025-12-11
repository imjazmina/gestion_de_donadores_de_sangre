const form = document.getElementById("login-form");
const tabDoctor = document.getElementById("tab-doctor");
const tabAdmin = document.getElementById("tab-admin");
const button = document.getElementById("login-button");

let currentRole = "doctor"; 


tabDoctor.addEventListener("click", () => {
  currentRole = "doctor";
  tabDoctor.classList.add("active");
  tabAdmin.classList.remove("active");
  button.textContent = "Ingresar como Personal Médico";
});

tabAdmin.addEventListener("click", () => {
  currentRole = "admin";
  tabAdmin.classList.add("active");
  tabDoctor.classList.remove("active");
  button.textContent = "Ingresar como Administrador";
});

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  // Credenciales predefinidas
  const doctorUser = { email: "test@gmail.com", password: "test123" };
  const adminUser = { email: "admin@gmail.com", password: "admin1234" };

  if (
    (currentRole === "doctor" &&
      email === doctorUser.email &&
      password === doctorUser.password)
  ) {
    alert("Bienvenido, Personal Médico");
    window.location.href = "admin\solicitudes.html";
  } else if (
    (currentRole === "admin" &&
      email === adminUser.email &&
      password === adminUser.password)
  ) {
    alert("Bienvenido, Administrador");
    window.location.href = "adminpanel.html";
  } else {
    alert("Credenciales incorrectas. Intente nuevamente.");
  }
});
