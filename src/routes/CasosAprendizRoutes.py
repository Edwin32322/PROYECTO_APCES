
from src.models.Casos import casosAprendiz
from ..services.CasosAprendizService import CasosAprendizService
from ..models.Forms import  *
import base64
from io import BytesIO
from flask import Blueprint, render_template, redirect, request, url_for, make_response, send_file, flash
from flask_login import login_required, current_user
from ..routes.wrappers.wrappers import decorador_rol_usuario, decorador_estado_usuario
from ..helpers.helpers import generate_password_and_user

#Blueprint para categorizar las rutas del usuario 
casos= Blueprint('casos_blueprint', __name__)

@casos.route("/crearCaso", methods=["POST", "GET"])
def crearCaso():
    formCrearCaso = FormularioCrearCasoAprendiz()
    if formCrearCaso.validate_on_submit() and request.method == "POST":
        caso = casosAprendiz(
            tipo_Documento = request.form["tipo_Documento"],
            num_Documento = request.form["num_Documento"],
            num_Ficha = request.form["num_Ficha"],
            nombre_Aprendiz = request.form["nombre_Aprendiz"],
            correo_Aprendiz = request.form["correo_Aprendiz"],
        )
        if(not CasosAprendizService.hay_un_caso_existente(caso)):
            CasosAprendizService.crear_caso_aprendiz(caso)
            flash("El caso ha sido registrado con éxito", "caso_registrado")
        else:
            flash("El aprendiz ya cuenta con un caso", "error_registro")
    return render_template("crearCaso.html", formCrearCaso = formCrearCaso)

@casos.route("/visualizarCasos")
def visualizarCasos():
    casos = CasosAprendizService.consultarCasosAprendiz()
    return render_template("visualizarCasos.html", casos = casos)


@casos.route("/modificarCaso/<int:id>", methods=["POST", "GET"])
def modificarCaso(id):
    formModificarCaso = FormularioCrearCasoAprendiz()
    modificarCaso = CasosAprendizService.consultar_caso_por_id(id)
    if formModificarCaso.validate_on_submit():
        if request.method == "POST":
            casoObj = casosAprendiz(
                id_CasoAprendiz= id,
                tipo_Documento= formModificarCaso.tipo_Documento.data,
                num_Documento= formModificarCaso.num_Documento.data,
                num_Ficha = formModificarCaso.num_Ficha.data,
                nombre_Aprendiz= formModificarCaso.nombre_Aprendiz.data,
                correo_Aprendiz= formModificarCaso.correo_Aprendiz.data
            )
            if(not CasosAprendizService.hay_un_caso_existente(casoObj)):
                flash("El caso ha sido modificado con éxito", "registro_exitoso")
                CasosAprendizService.actualizar_caso(casoObj)
            else:
                formModificarCaso.id_CasoAprendiz = id
                flash("El aprendiz ya cuenta con un caso", "error_registro")
                return render_template("modificarCaso.html", formModificarCaso = formModificarCaso) 
            return redirect(url_for("casos_blueprint.modificarCaso", id = id))
    else:     
        formModificarCaso.id_CasoAprendiz = id
        formModificarCaso.tipo_Documento.data = modificarCaso.tipo_Documento
        formModificarCaso.num_Documento.data = modificarCaso.num_Documento
        formModificarCaso.num_Ficha.data = int(modificarCaso.num_Ficha)
        formModificarCaso.nombre_Aprendiz.data = modificarCaso.nombre_Aprendiz
        formModificarCaso.correo_Aprendiz.data = modificarCaso.correo_Aprendiz
    return render_template("modificarCaso.html", formModificarCaso = formModificarCaso) 


