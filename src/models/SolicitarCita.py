class solicitarCitacion:
    def __init__(self, num_Ficha=None, nombre_Aprendiz=None, correo_Aprendiz=None,id_CasoAprendizFK = None) -> None:

        self.num_Ficha = num_Ficha
        self.nombre_Aprendiz = nombre_Aprendiz
        self.correo_Aprendiz = correo_Aprendiz
        self.id_CasoAprendizFK = id_CasoAprendizFK