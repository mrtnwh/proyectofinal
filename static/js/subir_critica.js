var idPelicula = document.getElementsByClassName("container")[0].id;
const form = document.getElementById('form-critica');

const token = localStorage.getItem('token');

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let data = {
        review_title: form.elements["title"].value,
        review_text: form.elements["review"].value
    }

    fetch(`/api/peliculas/${idPelicula}/subir_critica`, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok){
            window.location.href= `/peliculas/${idPelicula}`
        }
        else{
            window.location.href = '/login'
        }
    })
})
