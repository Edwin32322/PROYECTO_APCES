
from src.models.Llamado import Llamado
from src.services.CasosAprendizService import CasosAprendizService
from ..services.LlamadosService import LlamadosService
from ..models.Forms import  *
from io import BytesIO
from werkzeug.datastructures import FileStorage
from http import HTTPStatus
import base64
from io import BytesIO
from flask import Blueprint, render_template, redirect, request, url_for, make_response, send_file, flash
from flask_login import login_required, current_user
from ..routes.wrappers.wrappers import decorador_rol_usuario, decorador_estado_usuario
from ..helpers.helpers import generate_password_and_user


#Blueprint para categorizar las rutas del usuario 
calls= Blueprint('calls_blueprint', __name__)

@calls.route("/registrarLlamado", methods=["GET"])
def vistaRegistrarLlamado():
    consultarCasos = CasosAprendizService.consultarCasosAprendiz()
    return render_template("visualizarParaLlamado.html", casos = consultarCasos)
@calls.route("/visualizarLlamados")
def visualizarLlamados():
    llamados = LlamadosService.consultarLlamados()
    return render_template("visualizarLlamados.html", llamados = llamados)

@calls.route("/visualizarLlamado/<int:id>")
def visualizarLlamado(id):
    llamado = LlamadosService.consultar_llamado_por_id(id)
    plan_Mejora_base64 = base64.b64encode(llamado.plan_Mejora).decode('utf-8')
    llamado.plan_Mejora = 'data:application/pdf;base64,' + plan_Mejora_base64
    return render_template("visualizarLlamado.html", llamado = llamado)

@calls.route("/modificarLlamado/<int:id>", methods=["POST","GET"])
def modificarLlamado(id):
    formActualizar = FormularioRegistrarLlamado()
    modificarLamado = LlamadosService.consultar_llamado_por_id(id)
    if formActualizar.validate_on_submit():
        if request.method == "POST":
            llamadoObj = Llamado(
            id_LlamadoAtencion= id,
            num_Ficha = formActualizar.num_Ficha.data,
            nombre_Aprendiz = formActualizar.nombre_Aprendiz.data,
            correo_Aprendiz =  formActualizar.correo_Aprendiz.data,
            num_LlamadosAtencion = formActualizar.num_LlamadosAtencion.data,
            nombre_Instructor = formActualizar.nombre_Instructor.data,
            fecha = formActualizar.fecha.data,
            falta = formActualizar.falta.data,
            tipo_Falta= formActualizar.tipo_Falta.data,
            art_Incumplido = formActualizar.art_Incumplido.data,
            motivo = formActualizar.motivo.data,
            plan_Mejora = formActualizar.plan_Mejora.data.read(),
            firma_Instructor = formActualizar.firma_Instructor.data.read(),
            firma_Aprendiz = formActualizar.firma_Aprendiz.data.read(),
            firma_Vocero = formActualizar.firma_Vocero.data.read()
            )
            LlamadosService.actualizar_llamado(llamadoObj)
            return redirect(url_for("calls_blueprint.visualizarLlamados"))
    else:     
        formActualizar.id_LlamadoAtencion = id
        formActualizar.num_Ficha.data = modificarLamado.num_Ficha
        formActualizar.nombre_Aprendiz.data = modificarLamado.nombre_Aprendiz
        formActualizar.num_LlamadosAtencion.data = modificarLamado.num_LlamadosAtencion
        formActualizar.nombre_Instructor.data = modificarLamado.nombre_Instructor
        formActualizar.correo_Aprendiz.data = modificarLamado.correo_Aprendiz
        formActualizar.fecha.data = modificarLamado.fecha
        formActualizar.falta.data = modificarLamado.falta
        formActualizar.tipo_Falta.data = modificarLamado.tipo_Falta
        formActualizar.art_Incumplido.data = modificarLamado.art_Incumplido
        formActualizar.motivo.data = modificarLamado.motivo

    return render_template("modificarLlamado.html", formActualizar = formActualizar) 


@calls.route("/registrarLlamado/caso/<int:id>", methods=["POST","GET"])
def registrarLlamadoPorCaso(id):
    try:
        formRegistrar = FormularioRegistrarLlamado()
        caso = CasosAprendizService.consultar_caso_por_id(id)
        if formRegistrar.validate_on_submit():
            formRegistrar.id_CasoAprendiz = id
            if request.method == "POST":
                llamadoObj = Llamado(
                num_Ficha = formRegistrar.num_Ficha.data,
                nombre_Aprendiz = formRegistrar.nombre_Aprendiz.data,
                correo_Aprendiz =  formRegistrar.correo_Aprendiz.data,
                num_LlamadosAtencion = formRegistrar.num_LlamadosAtencion.data,
                nombre_Instructor = formRegistrar.nombre_Instructor.data,
                fecha = formRegistrar.fecha.data,
                falta = formRegistrar.falta.data,
                tipo_Falta= formRegistrar.tipo_Falta.data,
                art_Incumplido = formRegistrar.art_Incumplido.data,
                motivo = formRegistrar.motivo.data,
                plan_Mejora = formRegistrar.plan_Mejora.data.read(),
                firma_Instructor = formRegistrar.firma_Instructor.data.read(),
                firma_Aprendiz = formRegistrar.firma_Aprendiz.data.read(),
                firma_Vocero = formRegistrar.firma_Vocero.data.read()
                )
                LlamadosService.registrar_llamado(llamadoObj, caso, current_user)
                return redirect(url_for("calls_blueprint.visualizarLlamados"))
        else:     
            formRegistrar.id_CasoAprendiz = id
            formRegistrar.num_Ficha.data = caso.num_Ficha
            formRegistrar.nombre_Aprendiz.data = caso.nombre_Aprendiz
            formRegistrar.nombre_Instructor.data = current_user.nombre_Usuario
            formRegistrar.correo_Aprendiz.data = caso.correo_Aprendiz
            
    except AttributeError as e:
        flash("Caso inexistente. No se puede realizar llamados de atención a un aprendiz que no tiene un caso", "error_llave_foranea")
        return redirect(url_for("calls_blueprint.vistaRegistrarLlamado")) 
    
    return render_template("registrarLlamado.html", formRegistrar = formRegistrar) 
