const form = document.getElementById('form-login');

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let data = {
        email: form.elements["email"].value,
        password: form.elements["password"].value
    }

    fetch('/api/login', {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok){
            window.location.href= '/'
            console.log("Ingreso exitoso");
        }
        else{
            console.log("Ingreso fallido");
            document.getElementById('mensaje-error').innerHTML = 'Error al ingresar. Vuelva a intentarlo'
        }
    })
})