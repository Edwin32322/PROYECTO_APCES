class ArchivosLlamadosAtencion():
    def __init__(self, id_ArchivoLlamado = None, llamado_Atencion = None, fecha_Creacion = None, id_LlamadoAtencionFK = None) -> None:
        self.id_ArchivoLlamado = id_ArchivoLlamado
        self.llamado_Atencion = llamado_Atencion
        self.fecha_Creacion = fecha_Creacion
        self.id_LlamadoAtencionFK = id_LlamadoAtencionFK