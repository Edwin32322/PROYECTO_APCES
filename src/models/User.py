from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_Usuario = None, numero_Documento_Usuario = None, tipoDoc_Usuario  = None, telefono_Usuario = None, correo_Usuario = None, nombre_Usuario = None, contrasena_Usuario = None, imagen_Usuario = None, estado_Usuario = None, id_Rol_FK = None) -> None:
        self.id_Usuario = id_Usuario
        self.numero_Documento_Usuario = numero_Documento_Usuario
        self.tipoDoc_Usuario = tipoDoc_Usuario
        self.telefono_Usuario = telefono_Usuario
        self.correo_Usuario = correo_Usuario
        self.nombre_Usuario = nombre_Usuario
        self.contrasena_Usuario = contrasena_Usuario
        self.imagen_Usuario = imagen_Usuario
        self.estado_Usuario = estado_Usuario
        self.id_Rol_FK = id_Rol_FK
        
    def get_id(self):
        return str(self.id_Usuario)