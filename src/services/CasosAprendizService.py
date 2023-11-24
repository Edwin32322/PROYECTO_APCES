#Importamos la conexión a BD
from ..database.db_mysql import get_connection
from ..helpers.helpers import generate_password
from ..models.Casos import casosAprendiz 
from ..uploads.ModificarArchivos import modificar_template
class CasosAprendizService():

    @classmethod
    def crear_caso_aprendiz(cls, casoApren):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """INSERT INTO casosAprendiz (tipo_Documento, num_Documento, num_Ficha, nombre_Aprendiz, correo_Aprendiz) VALUES (%s, %s, %s, %s, %s)"""
                datos = (
                    casoApren.tipo_Documento,
                    casoApren.num_Documento,
                    casoApren.num_Ficha,
                    casoApren.nombre_Aprendiz,
                    casoApren.correo_Aprendiz,
    
                )
                cursor.execute(sql, datos)
                conexion.commit()
        except Exception as ex:
            raise ex
    
    @classmethod
    def consultar_caso_por_id(self, id):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM casosaprendiz WHERE id_CasoAprendiz = %s"
                cursor.execute(sql, (id,))
                caso = cursor.fetchone()
                if caso != None:
                    casoAprendizObj = casosAprendiz(
                        id_CasoAprendiz = caso[0],
                        tipo_Documento= caso[1],
                        num_Documento= caso[2],
                        num_Ficha= int(caso[3]),
                        programa_Formacion = caso[4],
                        nombre_Aprendiz= caso[5],
                        correo_Aprendiz= caso[6]
                    )
                    return casoAprendizObj
                else:
                    return None
        except Exception as ex:
            raise ex

        
    
        
    @classmethod
    def consultarCasosAprendiz(self):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM casosaprendiz"
                cursor.execute(sql)
                datos = cursor.fetchall()
                casos = []
                for row in datos:
                    datos = casosAprendiz(
                        id_CasoAprendiz = row[0],
                        tipo_Documento= row[1],
                        num_Documento= row[2],
                        num_Ficha= int(row[3]),
                        programa_Formacion = row[4],
                        nombre_Aprendiz= row[5],
                        correo_Aprendiz= row[6]
                    )

                    casos.append(datos)
                return casos
        except Exception as e:
            raise e
        
    @classmethod
    def actualizar_caso(cls, caso):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """UPDATE casosaprendiz SET tipo_Documento = %s, num_Documento = %s, nombre_Aprendiz = %s, num_Ficha = %s, correo_Aprendiz = %s WHERE id_CasoAprendiz = %s """
                datos = (
                    caso.tipo_Documento,
                    caso.num_Documento,
                    caso.nombre_Aprendiz,
                    caso.num_Ficha,
                    caso.correo_Aprendiz,
                    caso.id_CasoAprendiz
                )
                cursor.execute(sql, datos)
                conexion.commit()
                return True
        except Exception as ex:
            raise ex
    @classmethod
    def hay_un_caso_existente(self, caso):
        try:
            conexion = get_connection()
            with conexion.cursor() as cursor:
                sql = """SELECT * FROM casosaprendiz WHERE nombre_Aprendiz = %s AND num_Ficha = %s OR num_Documento = %s"""
                datos = (
                    caso.nombre_Aprendiz,
                    caso.num_Ficha,
                    caso.num_Documento
                )
                cursor.execute(sql, datos)
                resultado = cursor.fetchone()
                    
                if resultado is None:
                    return False
                else:
                    if resultado[0] == caso.id_CasoAprendiz:
                        return False
                    return True
                
        except Exception as ex:
            raise ex