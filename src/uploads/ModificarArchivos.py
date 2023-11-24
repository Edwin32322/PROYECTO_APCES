from io import BytesIO
import pythoncom
from pathlib import Path
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert  # Importa la función convert de docx2pdf
def covertir_a_pdf(temp_docx_path):
    try:
        pythoncom.CoInitialize()
        pdf_output_path = Path(__file__).parent.parent / "documents" / "temporales" / "DocumentoModificado.pdf"

        # Convierte el archivo DOCX temporal a PDF
        convert(temp_docx_path, pdf_output_path)
        return pdf_output_path
    except Exception as e:
        print(f"Error en la conversión a PDF: {e}")
        raise e
    finally:
        pythoncom.CoUninitialize()
        
def modificar_template(datos):
    try:
        pythoncom.CoInitialize()

        # Ruta de la plantilla existente
        template_path = Path(__file__).parent.parent / "documents" / "Llamado_Atencion.docx"

        # Ruta y nombre de archivo donde deseas guardar el documento modificado
        output_path = Path(__file__).parent.parent / "documents" / "temporales" / "DocumentoModificado.docx"

        # Cargar la plantilla existente
        doc = DocxTemplate(template_path)

        # Obtener el contenido de la imagen desde los datos
        img_Aprendiz = datos[12]
        img_Instructor = datos[11]
        img_Vocero = datos[13]

        # Crear objetos BytesIO para trabajar con el contenido de las imágenes
        img_AprendizByt = BytesIO(img_Aprendiz)
        img_InstructorByt = BytesIO(img_Instructor)
        img_VoceroByt = BytesIO(img_Vocero)

        # Crear objetos InlineImage
        imgAprendizCar = InlineImage(doc, img_AprendizByt, width=Mm(50), height=Mm(15))
        imgInstructorCar = InlineImage(doc, img_InstructorByt, width=Mm(50), height=Mm(15))
        imgVoceroCar = InlineImage(doc, img_VoceroByt, width=Mm(50), height=Mm(15) )

        # Agregar datos al contexto
        context = {
            "num_Ficha": datos[0],
            "nombre_Aprendiz": datos[1],
            "nombre_Instructor" : datos[4],
            "fecha": datos[5],
            "motivo": datos[9],
            "firma_Instructor" : imgInstructorCar,
            "firma_Aprendiz": imgAprendizCar,
            "firma_Vocero" : imgVoceroCar
        }

        # Renderizar la plantilla con los datos
        doc.render(context)

        # Guardar el documento modificado
        doc.save(output_path)
        return output_path  # Devuelve la ruta del documento DOCX generado
    except Exception as e:
        raise e
    finally:
        pythoncom.CoUninitialize()
