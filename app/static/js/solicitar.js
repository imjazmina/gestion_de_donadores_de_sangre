const contenedor = document.getElementById("cardsContainer");
const filtro = document.getElementById("filtroSangre");
const mensajeVacio = document.getElementById("mensajeVacio");


let donantes = []; // 

function mostrarCards(lista) {
  contenedor.innerHTML = "";
  
  if (lista.length === 0) {
    mensajeVacio.style.display = "block";
    return;
  }

  mensajeVacio.style.display = "none";

  lista.forEach(d => {
    const card = document.createElement("div");
    card.classList.add("card");
    card.innerHTML = `
      <div class="card-header">
        <h3>${d.nombre}</h3>
        <span class="etiqueta ${d.urgencia}">${d.urgencia}</span>
      </div>
      <div class="tipo-sangre"> Tipo: ${d.tipo}</div>
      <div class="info-extra">
        Edad: ${d.edad} años<br>
        Requiere: ${d.requiere}<br>
        Última donación: ${d.ultimaDonacion}
      </div>
      <div class="hospital"> <strong>${d.hospital}</strong><br>${d.ciudad}</div>
      <div class="botones">
        <button class="boton azul">Donar ahora</button>
        <button class="boton outline">Contactar</button>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

filtro.addEventListener("change", e => {
  const tipo = e.target.value;
  const filtrados = tipo === "todos" ? donantes : donantes.filter(d => d.tipo === tipo);
  mostrarCards(filtrados);
});

setTimeout(() => {
  donantes = []; 
  mostrarCards(donantes);
}, 500);
