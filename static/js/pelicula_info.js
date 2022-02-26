var idPelicula = document.getElementsByClassName('cont-info')[0].id;
var contInfoDcha = document.getElementById('cont-info-dcha');
var row1 = document.getElementById('row1');
var row2 = document.getElementById('row2')

fetch('http://127.0.0.1:5000/static/json/peliculas.json')
    .then(response => response.json())
    .then(data => 
        data.peliculas.forEach(peli => {
            if (peli.id == idPelicula) {
                contInfoDcha.innerHTML += `
                    <img src="${peli.poster}" alt="Poster de pelicula: ${peli.title}"> `

                row1.innerHTML += `
                    <h2>${peli.title}</h2>
                    <div>
                        <p>${peli.date} /</p>
                        <p>${peli.genre}</p>
                    </div> `

                row2.innerHTML += `
                    <h3>Sinopsis</h3>
                    <p>${peli.overview}</p>
                    <h3>Direccion</h3>
                    <p>${peli.director}</p> `
            }    
        })  
    )