
#Importamos la conexión a BD
from ..database.db_mysql import get_connection
from ..helpers.helpers import generate_password
from ..models.User import User


class LlamadosService():
    #Método para registrar un usuario
    
    @classmethod
    def consultarLlamados(self):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM LlamadoAtencion"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise e
        
    @classmethod
    def registrar_llamado(cls, llamado):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """INSERT INTO LlamadoAtencion (num_Ficha, nombre_Aprendiz, correo_Aprendiz, num_LlamadosAtencion, 
                        nombre_Instructor, fecha, falta, tipo_falta, art_incumplido, motivo, plan_Mejora, firma_Instructor, 
                        firma_Aprendiz, firma_Vocero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                datos = (
                    llamado.num_Ficha,
                    llamado.nombre_Aprendiz,
                    llamado.correo_Aprendiz,
                    llamado.num_LlamadosAtencion,
                    llamado.nombre_Instructor,
                    llamado.fecha,
                    llamado.falta,
                    llamado.tipo_Falta,
                    llamado.art_Incumplido,
                    llamado.motivo,
                    llamado.plan_Mejora,
                    llamado.firma_Instructor,
                    llamado.firma_Aprendiz,
                    llamado.firma_Vocero
                )
                cursor.execute(sql, datos)
                conexion.commit()
        except Exception as ex:
            raise ex
