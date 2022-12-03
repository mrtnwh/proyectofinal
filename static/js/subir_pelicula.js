const form = document.getElementById('form-subir');
const token = localStorage.getItem('token');

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let data = {
        title: form.elements["title"].value,
        director: form.elements["director"].value,
        date: form.elements["date"].value,
        poster: form.elements["poster-link"].value,
        overview: form.elements["overview"].value,
        genre: form.elements["genre"].value,
        trailer: form.elements["trailer"].value
    }

    console.log(data);

    fetch('/api/peliculas', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok){
            window.location.href= '/peliculas'
        }
        else{
            window.location.href = '/login'
        }
    })
})