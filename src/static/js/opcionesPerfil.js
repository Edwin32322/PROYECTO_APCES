document.addEventListener("DOMContentLoaded", () => {
    
    const perfilLink = document.getElementById('perfil-link');
    const opcionesPerfil = document.getElementById('opciones-perfil');
    
    // Agregar un evento de clic a la imagen del perfil
    perfilLink.addEventListener('click', (event) => {
        event.preventDefault();
        opcionesPerfil.classList.toggle('visible');
    });
    

    
});
