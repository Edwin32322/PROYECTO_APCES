#Importamos la conexión a BD
from datetime import timedelta

from src.models.Citacion import Citacion
from src.services.CasosAprendizService import CasosAprendizService
from ..database.db_mysql import get_connection
from ..helpers.helpers import generate_password
from ..models.Casos import casosAprendiz 
from ..uploads.ModificarArchivos import modificar_template

class CitacionesService():
    
    @classmethod
    def consultar_todas_las_citaciones(self):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """SELECT * FROM citacion"""
                cursor.execute(sql)
                row = cursor.fetchall()
                if row:
                    listaCitaciones = []
                    for citacion in row:
                        citacionObj = Citacion(
                            id_Citacion = citacion[0],
                            fecha_Citacion = citacion[1],
                            correo_Citacion = citacion[2],
                            hora_Citacion = citacion[3],
                            descripcion_Citacion = citacion[4],
                            asunto_Citacion = citacion[5],
                            destinatario = citacion[6],
                            id_CasoAprendizFK = citacion[7]
                        )
                        listaCitaciones.append(citacionObj)
                    return listaCitaciones
                else: 
                    return None
        except Exception as ex:
            raise ex
        
    @classmethod
    def solicitar_citacion(cls, solicitud):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """INSERT INTO solicitudcitacion (nombre_Aprendiz, correo_Aprendiz,id_CasoAprendizFK) VALUES (%s, %s, %s)"""
                datos = (
                    solicitud.nombre_Aprendiz,
                    solicitud.correo_Aprendiz,
                    solicitud.id_CasoAprendizFK
                )
                cursor.execute(sql, datos)
                conexion.commit()
        except Exception as ex:
            raise ex
        
    @classmethod
    def consultarAprendizParaCitacion(self):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """SELECT cita.motivo_ParaCitacion, caso.* FROM casoparacitacion cita INNER JOIN casosaprendiz caso ON id_CasoAprendizFK = id_CasoAprendiz;"""
                cursor.execute(sql)
                aprendicez = cursor.fetchall()

                if aprendicez:
                    return aprendicez
                else: 
                    None
        except Exception as ex:
            raise ex
    
    @classmethod
    def consultar_solicitudes(self):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """SELECT * FROM solicitudcitacion;"""
                cursor.execute(sql)
                solicitudes = cursor.fetchall()

                if solicitudes:
                    return solicitudes
                else: 
                    None
        except Exception as ex:
            raise ex
        
    @classmethod
    def consultar_citaciones_registradas(self):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """SELECT * FROM citacion WHERE destinatario = "Participantes" or id_CasoAprendizFK = NULL"""
                cursor.execute(sql)
                citacionesBd = cursor.fetchall()
                citaciones = []
                if citacionesBd:
                    for citacion in citacionesBd:
                        cita = Citacion(
                            id_Citacion = citacion[0],
                            fecha_Citacion = citacion[1],
                            correo_Citacion = citacion[2],
                            hora_Citacion = citacion[3],
                            descripcion_Citacion = citacion[4],
                            asunto_Citacion = citacion[5],
                            destinatario = citacion[6],
                            id_CasoAprendizFK = citacion[7] 
                        )
                        citaciones.append(cita)
                    return citaciones
                else:
                    return None
        except Exception as ex:
            raise ex
        
    @classmethod
    def consultar_existencia_citacion(self, citacion):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """SELECT * FROM citacion WHERE fecha_Citacion =  %s"""
                cursor.execute(sql, (citacion.fecha_Citacion,))
                citacion = cursor.fetchone()
                if citacion is not None:
                    return True
                else: 
                    return False
        except Exception as ex:
            raise ex
    @classmethod
    def consultar_existencia_citacion_rango(self, fecha):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                print(fecha)
                fecha_inferior = fecha - timedelta(days=30)
                fecha_superior = fecha + timedelta(days=30)
                cursor.execute("SELECT * FROM citacion WHERE fecha_Citacion BETWEEN %s AND %s", (fecha_inferior, fecha_superior))
                citas_en_rango = cursor.fetchall()
                return len(citas_en_rango) > 0
        except Exception as e:
            raise e
        # end try
    @classmethod
    def crear_citacion(self, citacion):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """INSERT INTO `citacion`(`fecha_Citacion`, `correo_Citacion`, `hora_Citacion`, `descripcion_Citacion`, `asunto_Citacion`, `destinatario`, `id_CasoAprendizFK`) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (citacion.fecha_Citacion, citacion.correo_Citacion, citacion.hora_Citacion, citacion.descripcion_Citacion, citacion.asunto_Citacion, "Participantes", citacion.id_CasoAprendizFK))
                conexion.commit()
                citacion = cursor.fetchone()
                if citacion is not None:
                    return True
                else: 
                    return False
        except Exception as ex:
            raise ex
        
    @classmethod
    def consultar_citacion(self, id_Citacion):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """SELECT * FROM citacion WHERE id_Citacion = %s"""
                cursor.execute(sql, (id_Citacion,))
                conexion.commit()
                citacion = cursor.fetchone()
                if citacion is not None:
                    return Citacion(
                        id_Citacion = citacion[0],
                        fecha_Citacion = citacion[1],
                        hora_Citacion = citacion[3]  
                    )
                else: 
                    return False
        except Exception as ex:
            raise ex