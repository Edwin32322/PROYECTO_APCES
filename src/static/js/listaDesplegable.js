document.addEventListener("DOMContentLoaded", () => {
    /* Función para desplegar las opciones de la barra desplegable */ 
    var listadesple = document.querySelectorAll('.opcion');
    listadesple.forEach(function(item){
        item.addEventListener('click', (i) => {
            var elemento = i.target.parentNode;
            elemento.children[1].classList.toggle('activo');
        })
    })
        
});