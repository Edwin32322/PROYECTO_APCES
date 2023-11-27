from io import BytesIO
import io
import pythoncom
from pathlib import Path
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert  # Importa la función convert de docx2pdf

import base64
import PyPDF2
def leer_pdf(documento_binario):

    # Decodificar el contenido binario
    contenido_decodificado = base64.b64decode(documento_binario)
    
    # Crear un objeto PyPDF2
    pdf_writer = PyPDF2.PdfWriter()
    
    # Agregar la página al archivo PDF
    pdf_writer.addPage(PyPDF2.PdfFileReader(io.BytesIO(contenido_decodificado)).getPage(0))
    
    # Crear un archivo temporal para almacenar el PDF convertido
    pdf_temporal = io.BytesIO()
    pdf_writer.write(pdf_temporal)
    
    # Obtener el contenido del archivo temporal
    pdf_temporal.seek(0)
    contenido_pdf_convertido = pdf_temporal.read()
    return contenido_pdf_convertido
    
    # Ahora, `contenido_pdf_convertido` contiene el contenido binario del archivo PDF convertido
    
    # Puedes adjuntar `contenido_pdf_convertido` al correo electrónico
    
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
        imgAprendizCar = InlineImage(doc, img_AprendizByt, width=Mm(50), height=Mm(30))
        imgInstructorCar = InlineImage(doc, img_InstructorByt, width=Mm(50), height=Mm(30))
        imgVoceroCar = InlineImage(doc, img_VoceroByt, width=Mm(50), height=Mm(30) )

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
