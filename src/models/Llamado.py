class Llamado:
    def __init__(self, id_LlamadoAtencion=None, num_Ficha=None, nombre_Aprendiz=None, correo_Aprendiz=None,
                 num_LlamadosAtencion=None, nombre_Instructor=None, fecha=None, falta=None, tipo_Falta=None,
                 art_Incumplido=None, motivo=None, plan_Mejora=None, firma_Instructor=None, firma_Aprendiz=None,
                 firma_Vocero=None) -> None:
        self.id_LlamadoAtencion = id_LlamadoAtencion
        self.num_Ficha = num_Ficha
        self.nombre_Aprendiz = nombre_Aprendiz
        self.correo_Aprendiz = correo_Aprendiz
        self.num_LlamadosAtencion = num_LlamadosAtencion
        self.nombre_Instructor = nombre_Instructor
        self.fecha = fecha
        self.falta = falta
        self.tipo_Falta = tipo_Falta
        self.art_Incumplido = art_Incumplido
        self.motivo = motivo
        self.plan_Mejora = plan_Mejora
        self.firma_Instructor = firma_Instructor
        self.firma_Aprendiz = firma_Aprendiz
        self.firma_Vocero = firma_Vocero
