document.addEventListener("DOMContentLoaded", () => {
        //Función para filtrar los roles
        const rol = document.getElementById("rol_usuario");
        console.log(rol)
        const usuarios = document.querySelectorAll(".lista ul a li");
        
        const cambiarRol = () => { 
            var rolSeleccionado = rol.value;
            usuarios.forEach(function(usuario) {
                var rolUsuario = usuario.getAttribute("data-rol");
                if(rolUsuario === '1'){
                    rolUsuario = 'Administrador'
                }else if(rolUsuario == '2'){
                    rolUsuario = 'Instructor'
                }
                console.log(rolUsuario)
                if (rolSeleccionado === "todos" || rolSeleccionado === rolUsuario) {
                    usuario.style.display = "flex";
                } else {
                    usuario.style.display = "none";
                }
            });
        };
        rol.addEventListener('change', cambiarRol)    
});