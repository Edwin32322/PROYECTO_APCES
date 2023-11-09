from functools import wraps
from ...services.AuthService import AuthService
from ...services.UserService import UserService
from flask import jsonify
from flask_login import current_user, logout_user

#Decorador personalizado para manejar los roles en las respectivas rutas
def decorador_rol_usuario(rol):
    def decorador(func):
        @wraps(func)
        def wrapp(*args, **kwargs):
            usuario = current_user
            if not UserService.usuario_rol(rol, usuario):
                return jsonify({
                    'Error' : 'Acceso denegeado',
                    'Message' : 'Está página está restringida para administradores'
                })
            return func(*args, **kwargs)
        return wrapp
    return decorador

#Decorador personalizado utilizado para saber el estado del usuario

#Esto es por si el usuario es inhabilitado mientras está en sesión, por lo que ya no podrá interactuar con el sistema
def decorador_estado_usuario():
    def decorador(func):
        @wraps(func)
        def wrapp(*args, **kwargs):
            sesionUsuario = current_user
            usuario = AuthService.get_by_id(sesionUsuario.id_Usuario)
            if not usuario.estado_Usuario == 1:
                logout_user()
                return jsonify({
                    'Error' : 'Acceso denegeado',
                    'Message' : 'El usuario ha sido inhabilitado'
                })
            return func(*args, **kwargs)
        return wrapp
    return decorador