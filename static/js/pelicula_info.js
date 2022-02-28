var idPelicula = document.getElementsByClassName("cont-info")[0].id;
var contInfoDcha = document.getElementById("cont-info-dcha");
var row1 = document.getElementById("row1");
var row2 = document.getElementById("row2");

fetch("/static/json/peliculas.json")
  .then((response) => response.json())
  .then((data) =>
    data.peliculas.forEach((peli) => {
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
