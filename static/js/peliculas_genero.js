var genero = document.getElementsByClassName('titulo')[0].id;
var container = document.getElementById('container-peli-generos')
var containerCards = document.getElementById('cont-cards-peli-generos');
var resultado = false

fetch('/static/json/peliculas.json')
    .then(response => response.json())
    .then(data => {
        data.peliculas.slice().reverse().forEach(peli => {
            if (peli.genre == genero) {
                resultado = true
                containerCards.innerHTML += 
                `
                    <div class="card-container">
                    <div class="card-img" style="background-image: url(${peli.poster});"></div>
                    <div class="card-content">

                        <div class="col1">
                            <h1>${peli.title}</h1>
                            <ul>
                                <li>${peli.date} /</li>
                                <li>${peli.genre}</li>
                            </ul>
                        </div>
                        
                        <div class="col2 sinopsis-fila">
                            <h4>SINOPSIS</h4>
                        </div>

                        <div class="col1 sinopsis-texto">
                            <p>${peli.overview}</p>
                        </div>
                        
                        <div class="col1">
                            <h5 class="director">${peli.director}</h5>
                        </div>

                        <div class="col1">
                            <button><a href="/peliculas/${peli.id}">Ver mas</a></button>
                        </div> 
                    </div>
                </div>
                ` 
            }
        })

        if (resultado === false) {
            container.innerHTML += 
            `   
            <div id="cont-not-found">
                <img src="/static/img/no-result-found.png" id="img-not-found">
                <h1 id="msj-not-found">No se encontró ningún resultado.</h1>
            </div>
            `
        }
    }    
)