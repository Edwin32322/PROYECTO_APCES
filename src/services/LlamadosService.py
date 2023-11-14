
#Importamos la conexión a BD
from ..database.db_mysql import get_connection
from ..helpers.helpers import generate_password
from ..models.Llamado import Llamado 


class LlamadosService():
    #Método para registrar un usuario
    
    @classmethod
    def consultarLlamados(self):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM LlamadoAtencion"
                cursor.execute(sql)
                row = cursor.fetchall()
                llamados = []
                for llamado in row:
                    object_call = Llamado(
                        id_LlamadoAtencion = llamado[0],
                        num_Ficha = llamado[1],
                        nombre_Aprendiz = llamado[2],
                        correo_Aprendiz = llamado[3],
                        num_LlamadosAtencion = llamado[4],
                        nombre_Instructor = llamado[5],
                        fecha = llamado[6],
                        falta = llamado[7],
                        art_Incumplido = llamado[8],
                        motivo = llamado[9],
                        plan_Mejora = llamado[10],
                        firma_Instructor = llamado[11],
                        firma_Aprendiz = llamado[11],
                        firma_Vocero = llamado[12]    
                    )
                    llamados.append(object_call)
                return llamados
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
