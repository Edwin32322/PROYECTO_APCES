
#Importamos la conexión a BD
from ..database.db_mysql import get_connection
from ..helpers.helpers import generate_password
from ..models.User import User
class UserService():
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
        
    @classmethod
    def actualizar_usuario(self, user):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                sql = """UPDATE Usuario SET 
                numero_Documento_Usuario = %s,
                tipoDoc_Usuario = %s,
                telefono_Usuario = %s,
                correo_Usuario = %s,
                nombre_Usuario = %s,
                estado_Usuario = %s,
                id_Rol_FK = %s
                WHERE id_Usuario = %s"""
                datos = (user.numero_Documento_Usuario,
                         user.tipoDoc_Usuario,
                         user.telefono_Usuario,
                         user.correo_Usuario,
                         user.nombre_Usuario,
                         user.estado_Usuario,
                         user.id_Rol_FK,
                         user.id_Usuario)
                print(datos)
                cursor.execute(sql, datos)
                conexion.commit()
                print('ACTUALIZACION EXITOSA')
                return user
        except Exception as ex:
            raise ex
    @classmethod
    def cambiar_imagen_usuario(self, user):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                sql = 'UPDATE Usuario SET imagen_Usuario = %s WHERE id_Usuario = %s'
                datos = (user.imagen_Usuario, user.id_Usuario)
                cursor.execute(sql, datos)
                conexion.commit()
                print('ACTUALIZACION EXITOSA')
                return user
        except Exception as ex:
            raise ex
        
    # end def
        
    @classmethod
    def cambiar_contra(self, user):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                sql = 'UPDATE Usuario SET contrasena_Usuario = %s WHERE id_Usuario = %s'
                datos = (user.contrasena_Usuario, user.id_Usuario)
                print(datos)
                cursor.execute(sql, datos)
                conexion.commit()
                print('ACTUALIZACION EXITOSA')
                return user
        except Exception as ex:
            raise ex
        
        
    #Método para modificar el estado del usuario 
    @classmethod
    def modificar_estado_usuario(self, user, opcion):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                consulta = 'SELECT estado_Usuario FROM Usuario WHERE id_Usuario = %s'
                cursor.execute(consulta, (user.id_Usuario,))
                row = cursor.fetchone()
                estado = 1 if opcion == 'activar' else 0
                if row[0] == estado:
                    return False
                else:
                    sql = 'UPDATE Usuario SET estado_Usuario = %s WHERE id_Usuario = %s'
                    datos = (estado, user.id_Usuario)
                    cursor.execute(sql, datos)
                    conexion.commit()
                    return True
        except Exception as ex:
            raise ex
                
    #Método para obtener los usuarios
    @classmethod
    def obtener_usuarios(self):
        conexion = get_connection()
        with conexion.cursor() as cursor:
            sql = ('SELECT id_Usuario, numero_Documento_Usuario, tipoDoc_Usuario, correo_Usuario, nombre_Usuario, estado_Usuario, id_Rol_FK FROM Usuario')
            cursor.execute(sql)
            row = cursor.fetchall()
            users = []
            for user in row:
                object_user = User(
                    id_Usuario = user[0],
                    numero_Documento_Usuario = user[1],
                    tipoDoc_Usuario = user[2],
                    correo_Usuario = user[3],
                    nombre_Usuario= user[4],
                    estado_Usuario= user[5],
                    id_Rol_FK = user[6]
                )
                users.append(object_user)
            return users
    
    #Método para si el usuario tiene un rol en específico (va de la mano con el wrapper personalizado decorador_rol_personalizado)
    @classmethod
    def usuario_rol(self, rol, user):
        conexion = get_connection()
        with conexion.cursor() as cursor:
            rol = 1 if rol == 'Administrador' else 2
            sql = ('SELECT id_Rol_FK FROM Usuario WHERE id_Usuario = %s')
            datos = (user.id_Usuario,)
            cursor.execute(sql, datos)
            row = cursor.fetchone()
            if row[0] == rol:
                return True
            else:
                return False
            
    #Método para saber si el correo que se intenta registrar en registrar usuarios ya existe en la BD
    @classmethod
    def checkear_email_en_bd(self, user):
        conexion = get_connection()
        with conexion.cursor() as cursor:
            sql = 'SELECT * FROM Usuario WHERE correo_Usuario = "{}"'.format(user.correo_Usuario)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is None:
                return True
            else:
                return False
    @classmethod
    def checkear_doc_en_bd(self, user):
        conexion = get_connection()
        with conexion.cursor() as cursor:
            sql = 'SELECT * FROM Usuario WHERE numero_Documento_Usuario= "{}"'.format(user.numero_Documento_Usuario)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is None:
                return True
            else:
                return False
        

