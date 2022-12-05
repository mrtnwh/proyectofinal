const dataPelicula = JSON.parse(document.querySelector(".container").dataset.pelicula)[0];

document.querySelector("#img-poster").setAttribute("src", `${dataPelicula.poster}`);
document.querySelector("#poster-link").setAttribute("value", `${dataPelicula.poster}`);
document.querySelector("#titulo").setAttribute("value", `${dataPelicula.title}`);
document.querySelector("#anio").setAttribute("value", `${dataPelicula.date}`);
document.querySelector("#link_trailer").setAttribute("value", `${dataPelicula.trailer}`);
document.querySelector("#sinopsis").innerHTML =`${dataPelicula.overview}`;

const idPelicula = dataPelicula.id;
const form = document.getElementById('form-editar');

const token = localStorage.getItem('token');

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let data = {
        title: form.elements["title"].value,
        director: form.elements["director"].value,
        date: form.elements["date"].value,
        poster: form.elements["poster"].value,
        overview: form.elements["overview"].value,
        genre: form.elements["genre"].value,
        trailer: form.elements["trailer"].value
    }

    fetch(`/api/peliculas/${dataPelicula.id}`, {
        method: 'PUT', 
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok){
            window.location.href= `/peliculas/${dataPelicula.id}`
        }
        else{
            window.location.href = '/login'
        }
    })
})