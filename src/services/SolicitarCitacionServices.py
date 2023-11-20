#Importamos la conexión a BD
from ..database.db_mysql import get_connection
from ..helpers.helpers import generate_password
from ..models.Casos import casosAprendiz 
from ..uploads.ModificarArchivos import modificar_template

class SolicitarCitacionService():

    @classmethod
    def solicitar_citacion(cls, solicitud):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """INSERT INTO soliictarCitacion (num_Ficha, nombre_Aprendiz, correo_Aprendiz, llamados) VALUES (%s, %s, %s, %s)"""
                datos = (
                    solicitud.num_Ficha,
                    solicitud.nombre_Aprendiz,
                    solicitud.correo_Aprendiz,
                    solicitud.llamados
    
                )
                cursor.execute(sql, datos)
                if modificar_template(datos):
                    print("ARCHIVO CREADO CON EXITO")
                else: 
                    print("Se presentó un error")
                conexion.commit()
        except Exception as ex:
            raise ex