const form = document.getElementById('form-subir');
const token = localStorage.getItem('token');

  const options = {
    method: "GET",
    headers: {
      "X-RapidAPI-Key": "911f45f642msha09b50099416e9fp1a5ce3jsn86155db597e7",
      "X-RapidAPI-Host": "imdb8.p.rapidapi.com",
    },
  };
  fetch(
    `https://imdb8.p.rapidapi.com/auto-complete?q=${form.elements["title"].value}`,
    options
  )
    .then((response) => response.json())
    .then((response) => (imageUrl = response.d[1].i.imageUrl))
    .then(() => console.log(imageUrl))
    .catch((err) => console.error(err));

  
form.addEventListener('submit', (e) => {
  e.preventDefault()

  var data = {
    title: form.elements["title"].value,
    director: form.elements["director"].value || form.elements["director-custom"].value,
    date: form.elements["date"].value,
    poster: imageUrl,
    overview: form.elements["overview"].value,
    genre: form.elements["genre"].value,
    trailer: form.elements["trailer"].value
  };

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