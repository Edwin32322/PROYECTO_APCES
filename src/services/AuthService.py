#Importamos la conexión a la base de datos
from ..database.db_mysql import get_connection
from ..helpers.helpers import check_password
from ..models.User import User


class AuthService():
    #Método que valida si el usuario existe en la base de datos
    @classmethod
    def login_user(cls, user):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Usuario WHERE correo_Usuario = %s', (user.correo_Usuario,))
                row = cursor.fetchone()
                if row != None:
                    authenticated_user = User(id_Usuario=row[0],
                                              numero_Documento_Usuario=row[1],
                                              tipoDoc_Usuario=row[2],
                                              telefono_Usuario= row[3],
                                              correo_Usuario=row[4],
                                              nombre_Usuario=row[5],
                                              contrasena_Usuario = check_password(row[6], user.contrasena_Usuario),
                                              imagen_Usuario= row[7],
                                              estado_Usuario=row[8],
                                              id_Rol_FK=row[9])
            return authenticated_user
        except Exception as ex:
            raise ex
        
    @classmethod
    def get_by_email(self, correo_Usuario):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = "SELECT id_Usuario from Usuario Where correo_Usuario = '{}'".format(correo_Usuario)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row is not None:
                    return User(id_Usuario=row[0])
        except  Exception as ex:
            raise Exception(ex)
        
    #Método que obtiene al usuario por su id y regresa un objeto
    @classmethod
    def get_by_id(self, id):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = "SELECT * from Usuario Where id_Usuario = '{}'".format(id)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row is not None:
                    return User(id_Usuario=row[0], 
                            numero_Documento_Usuario=row[1], 
                            tipoDoc_Usuario=row[2],
                            telefono_Usuario= row[3],
                            correo_Usuario=row[4], 
                            nombre_Usuario=row[5], 
                            contrasena_Usuario=row[6],
                            imagen_Usuario= row[7],
                            estado_Usuario=row[8],
                            id_Rol_FK=row[9])
        except  Exception as ex:
            raise Exception(ex)