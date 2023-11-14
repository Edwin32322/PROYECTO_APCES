document.addEventListener("DOMContentLoaded", () => {
    const filtrarAprendiz = document.getElementById("filtrarAprendiz");
    const filtrarFecha = document.getElementById("filtrarFecha");
    const usuarios = document.querySelectorAll(".lista ul li");

    const filtrarPorNombreYFecha = () => {
        const nombre = filtrarAprendiz.value.toLowerCase();
        const fechaSeleccionada = filtrarFecha.value;

        usuarios.forEach(function(usuario) {
            const nombreAprendiz = usuario.getAttribute("data-name").toLowerCase();
            const fecha = usuario.getAttribute("data-date");

            const cumpleNombre = nombre === "" || nombreAprendiz.includes(nombre);
            const cumpleFecha = fechaSeleccionada === "" || fechaSeleccionada == fecha;

            if (cumpleNombre && cumpleFecha) {
                usuario.style.display = "flex";
            } else {
                usuario.style.display = "none";
            }
        });
    };

    filtrarAprendiz.addEventListener('input', filtrarPorNombreYFecha);
    filtrarFecha.addEventListener('change', filtrarPorNombreYFecha);
});
