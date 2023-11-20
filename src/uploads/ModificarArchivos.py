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
        output_path = Path(__file__).parent.parent / "documents" / "temporales" /"DocumentoModificado.docx"

        # Cargar la plantilla existente
        doc = DocxTemplate(template_path)

        # Obtener el contenido de la imagen desde los datos
        img_Aprendiz = datos[12]
        img_Instructor = datos[11]
        img_Vocero = datos[13]
        # Crear un objeto BytesIO para trabajar con el contenido de la imagen
        img_AprendizByt = BytesIO(img_Aprendiz)
        img_InstructorByt = BytesIO(img_Instructor)
        img_VoceroByt = BytesIO(img_Vocero)
        # Crear un objeto InlineImage
        imgAprendizCar = InlineImage(doc, img_AprendizByt, width=Mm(50), height=Mm(15))
        imgInstructorCar = InlineImage(doc, img_InstructorByt, width=Mm(50), height=Mm(15))
        imgVoceroCar = InlineImage(doc, img_VoceroByt, width=Mm(50), height=Mm(15) )
        # Agregar datos al contexto
        context = {
            "fecha": datos[5],
            "nombre_Aprendiz": datos[1],
            "nombre_Instructor" : datos[4],
            "num_Ficha": datos[0],
            "motivo": datos[9],
            "firma_Aprendiz": imgAprendizCar,
            "firma_Instructor" : imgInstructorCar,
            "firma_Vocero" : imgVoceroCar
        }

        # Renderizar la plantilla con los datos
        doc.render(context)

        # Guardar el documento modificado
        doc.save(output_path)

        # Convertir el documento Word a PDF
        pdf_output_path = Path(__file__).parent.parent / "documents" / "temporales" / "DocumentoModificado.pdf"
        convert(output_path, pdf_output_path)

        return pdf_output_path  # Devuelve la ruta del PDF generado
    except Exception as e:
        raise e
