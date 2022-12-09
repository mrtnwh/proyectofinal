var idPelicula = document.getElementsByClassName("cont-info")[0].id;
var contInfoDcha = document.getElementById("cont-info-dcha");
var row1 = document.getElementById("row1");
var row2 = document.getElementById("row2");
const token = localStorage.getItem('token')

fetch("/api/peliculas")
  .then((response) => response.json())
  .then((data) =>
    data.forEach((peli) => {
      if (peli.id == idPelicula) {
        contInfoDcha.innerHTML += `
                    <img src="${peli.poster}" class="poster" alt="Poster de pelicula: ${peli.title}"> `;

        row1.innerHTML += `
                    <h2>${peli.title}</h2>
                    <div>
                        <p>Fecha de estreno: ${peli.date} </p>
                        <p>Genero: <b> ${peli.genre} </b> </p>
                    </div> `;

        row2.innerHTML += `
                    <h3>Sinopsis</h3>
                    <p class="sinopsis">${peli.overview}</p>
                    <h3>Direccion</h3>
                    <p>${peli.director}</p> 
                    <h3>Trailer</h3>
                    <iframe width="560" height="315" src="${peli.trailer}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
      }
    })
  );

var contCriticas = document.getElementById("cont-cards-criticas");
var msjNoCriticas = document.getElementById("no-hay-criticas");

fetch("/api/criticas")
  .then((response) => response.json())
  .then((data) =>
    data.slice().reverse().forEach((peli) => {
      if (peli.id == idPelicula) {

        msjNoCriticas.remove()

        peli.reviews.forEach((critica) => {
          contCriticas.innerHTML += `
            <div class="card-criticas">
              <h4 class="card-criticas-titulo">${critica.review_title}</h4>
              <p>Escrito por ${critica.user}</p>
              <div class="card-criticas-texto">
                  <p>${critica.review_text}</p>
              </div>
              <p class="light-gray">Publicado el ${critica.date}</p>
            </div> `
        })
      }
    })
  )

const btnDelete = document.getElementById('btn-delete');

btnDelete.addEventListener('click', (e) => {
  let clickDelete = e.target.id == "btn-delete"

  if (clickDelete) {
      fetch(`/api/peliculas/${idPelicula}`, {
          method: 'DELETE',
          headers: {'Authorization': `Bearer ${token}`}
      })
      .then(response => {
        if (response.ok) {
          window.location.href= "/peliculas";
        }
        else{
          alert("No se puede borrar. Hay criticas de usuarios.");
        }
      })
  }
})