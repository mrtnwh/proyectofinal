const cargarGeneros = async() => {
    try {
        const responseGeneros = await fetch('https://www.mockachino.com/e87585d1-9630-4f/generos');
        let selector = document.getElementById('nombre-generos'); 

        if(responseGeneros.status === 200){
            const jsonGeneros = await responseGeneros.json();

            jsonGeneros.generos.forEach(genero => {
                var nombre = genero.name;
                opcion = new Option(nombre, nombre);

                selector.insertAdjacentElement("beforeend", opcion);
            }); 
        }
    }
    catch(error) {
        console.log(error);
    }
}

const cargarDirectores = async() => {
    try {
        const responseDirectores = await fetch('https://www.mockachino.com/e87585d1-9630-4f/directores');
        let selector = document.getElementById('nombre-directores'); 

        if(responseDirectores.status === 200){
            const jsonDirectores = await responseDirectores.json();

            jsonDirectores.directores.forEach(director => {
                var nombre = director.name;
                opcion = new Option(nombre, nombre);

                selector.insertAdjacentElement("beforeend", opcion);
            }); 
        }
    }
    catch(error) {
        console.log(error);
    }
}





