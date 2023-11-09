
#Importamos la conexión a BD
from ..database.db_mysql import get_connection
from ..helpers.helpers import generate_password
from ..models.User import User


class LlamadosService():
    #Método para registrar un usuario
    @classmethod
    def registrar_usuario(self, user):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """INSERT INTO Usuario (id_Usuario, numero_Documento_Usuario, tipoDoc_Usuario, telefono_Usuario, correo_Usuario, nombre_Usuario, contrasena_Usuario
                , imagen_Usuario, estado_Usuario, id_Rol_FK) values(%s,
                %s, %s, %s, %s, %s, %s, %s ,%s, %s)"""
                datos = (
                    user.id_Usuario, 
                    user.numero_Documento_Usuario, 
                    user.tipoDoc_Usuario, 
                    user.telefono_Usuario,
                    user.correo_Usuario, 
                    user.nombre_Usuario, 
                    generate_password(user.contrasena_Usuario), 
                    user.imagen_Usuario,
                    user.estado_Usuario,
                    user.id_Rol_FK
                )
                cursor.execute(sql, datos)
                conexion.commit()
        except Exception as ex:
            raise ex
    