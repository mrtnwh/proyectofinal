var idPelicula = document.getElementsByClassName("container")[0].id;
console.log(idPelicula);

var urlCritica = `/peliculas/${idPelicula}/subir_critica`

document.getElementById("formCritica").action = urlCritica;

console.log(urlCritica);
console.log(document.getElementById("formCritica"));
