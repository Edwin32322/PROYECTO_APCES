class Citacion():
    def __init__(self,id_Citacion = None ,fecha_Citacion = None ,correo_Citacion = None ,hora_Citacion = None ,descripcion_Citacion = None ,asunto_Citacion = None ,destinatario = None ,id_CasoAprendizFK = None) -> None:
        self.id_Citacion = id_Citacion
        self.fecha_Citacion = fecha_Citacion
        self.correo_Citacion = correo_Citacion
        self.hora_Citacion = hora_Citacion
        self.descripcion_Citacion = descripcion_Citacion
        self.asunto_Citacion = asunto_Citacion
        self.destinatario = destinatario
        self.id_CasoAprendizFK = id_CasoAprendizFK
    