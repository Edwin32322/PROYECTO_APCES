
document.addEventListener("DOMContentLoaded", () => {
    const filtrarAprendiz = document.getElementById("filtrarAprendiz");
    const usuarios = document.querySelectorAll(".lista ul li");

    const filtrarPorNombre= () => {
        const nombre = filtrarAprendiz.value.toLowerCase();

        usuarios.forEach(function(usuario) {
            const nombreAprendiz = usuario.getAttribute("data-name").toLowerCase();
            const cumpleNombre = nombre === "" || nombreAprendiz.includes(nombre);

            if (cumpleNombre) {
                usuario.style.display = "flex";
            } else {
                usuario.style.display = "none";
            }
        });
    };

    filtrarAprendiz.addEventListener('input', filtrarPorNombre);
});
