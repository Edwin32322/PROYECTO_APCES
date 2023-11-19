from io import BytesIO
import pythoncom
from pathlib import Path
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert  # Importa la función convert de docx2pdf
def modificar_template(datos):
    try:
        pythoncom.CoInitialize()

        # Ruta de la plantilla existente
        template_path = Path(__file__).parent.parent / "documents" / "Llamado_Atencion.docx"

        # Ruta y nombre de archivo donde deseas guardar el documento modificado
        output_path = Path(__file__).parent.parent / "documents" / "DocumentoModificado.docx"

        # Cargar la plantilla existente
        doc = DocxTemplate(template_path)

        # Obtener el contenido de la imagen desde los datos
        img_stream = datos[13]

        # Crear un objeto BytesIO para trabajar con el contenido de la imagen
        img_bytesio = BytesIO(img_stream)

        # Crear un objeto InlineImage
        img = InlineImage(doc, img_bytesio, width=Mm(50), height=Mm(15))

        # Agregar datos al contexto
        context = {
            "fecha": datos[0],
            "nombre_Aprendiz": datos[1],
            "num_Ficha": datos[2],
            "motivo": datos[3],
            "firma_Aprendiz": img,
        }

        # Renderizar la plantilla con los datos
        doc.render(context)

        # Guardar el documento modificado
        doc.save(output_path)

        # Convertir el documento Word a PDF
        pdf_output_path = Path(__file__).parent.parent / "documents" / "DocumentoModificado.pdf"
        convert(output_path, pdf_output_path)

        return pdf_output_path  # Devuelve la ruta del PDF generado
    except Exception as e:
        raise e
