const dataPelicula = JSON.parse(document.querySelector(".container").dataset.pelicula)[0]

document.querySelector("#img-poster").setAttribute("src", `${dataPelicula.poster}`)
document.querySelector("#titulo").setAttribute("placeholder", `${dataPelicula.title}`)
document.querySelector("#anio").setAttribute("value", `${dataPelicula.date}`)
document.querySelector("#link_trailer").setAttribute("placeholder", `${dataPelicula.trailer}`)
document.querySelector("#sinopsis").innerHTML =`${dataPelicula.overview}`