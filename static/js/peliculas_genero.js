var genero = document.getElementsByClassName('titulo')[0].id;
var container = document.getElementById('container-peli-generos')
var containerCards = document.getElementById('cont-cards-peli-generos');
var resultado = false

fetch('http://127.0.0.1:5000/static/json/peliculas.json')
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
                            <button>Ver mas</button>
                        </div> 
                    </div>
                </div>
                ` 
            }
        })

        if (resultado === false) {
            container.innerHTML += 
            `
                <h1 style="color: black;">No se encontró ningun resultado :(</h1>
            `
        }
    }    
)