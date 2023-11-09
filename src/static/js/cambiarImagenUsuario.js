document.addEventListener("DOMContentLoaded", () => {
    const formularioImagen = document.getElementById("formulario-imagen");
    
    const toggleFormImagen = () => {
        formularioImagen.style.display = (formularioImagen.style.display === "block") ? "none" : "block";
    }
    
    const cambiarImagen = document.getElementById("cambiar-imagen")
    cambiarImagen.addEventListener("click", toggleFormImagen)
    
    const validarImagen = (event) => {
        const imagenInput = document.getElementById("nueva-imagen");
        if (!imagenInput.files.length) {
            event.preventDefault(); // Evitar el envío del formulario si no se selecciona una imagen
            alert("Por favor, seleccione una imagen antes de guardar.");
        }
    }
    const guardarImagen = document.getElementById("guardar-imagen")
    guardarImagen.addEventListener("click", validarImagen)
});

