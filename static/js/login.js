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
            console.log("Ingreso exitoso");
            window.location.href= '/'
        }
        else{
            document.getElementById('mensaje-error').innerHTML = 'Error al ingresar.';
        }

        return response.json()
    })
    .then(data => {
        localStorage.setItem("token", data.token);
    })

})