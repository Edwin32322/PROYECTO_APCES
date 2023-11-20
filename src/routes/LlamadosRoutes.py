
from src.models.Llamado import Llamado
from ..services.LlamadosService import LlamadosService
from ..models.Forms import  *
from io import BytesIO
from werkzeug.datastructures import FileStorage

import base64
from io import BytesIO
from flask import Blueprint, render_template, redirect, request, url_for, make_response, send_file
from flask_login import login_required, current_user
from ..routes.wrappers.wrappers import decorador_rol_usuario, decorador_estado_usuario
from ..helpers.helpers import generate_password_and_user


#Blueprint para categorizar las rutas del usuario 
calls= Blueprint('calls_blueprint', __name__)

@calls.route("/registrarLlamado", methods=["POST", "GET"])
def registrarLlamado():
    formRegistrarLlamado = FormularioRegistrarLlamado()
    if formRegistrarLlamado.validate_on_submit() and request.method == "POST":
        llamado = Llamado(
            None,
            num_Ficha = request.form["num_Ficha"],
            nombre_Aprendiz = request.form["nombre_Aprendiz"],
            correo_Aprendiz = request.form["correo_Aprendiz"],
            num_LlamadosAtencion = request.form["num_LlamadosAtencion"],
            nombre_Instructor = request.form["nombre_Instructor"],
            fecha = request.form["fecha"],
            falta = request.form["falta"],
            tipo_Falta= request.form["tipo_Falta"],
            art_Incumplido = request.form["art_Incumplido"],
            motivo = request.form["motivo"],
            plan_Mejora = request.files["plan_Mejora"].read(),
            firma_Instructor = request.files["firma_Instructor"].read(),
            firma_Aprendiz = request.files["firma_Aprendiz"].read(),
            firma_Vocero = request.files["firma_Vocero"].read()
        )
        
        LlamadosService.registrar_llamado(llamado)
        
        
        return redirect(url_for("calls_blueprint.visualizarLlamados"))

    return render_template("registrarLlamado.html", formRegistrarLlamado = formRegistrarLlamado)

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
        formActualizar.num_Ficha.data = int(modificarLamado.num_Ficha)
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



# @calls.route("/modificarLlamado/<int:id>", methods=["POST","GET"])
# def modificarLlamado(id):
#     formActualizar = FormularioRegistrarLlamado()
#     modificarLamado = LlamadosService.consultar_llamado_por_id(id)
#     if modificarLamado != None:
#         formActualizar.num_Ficha.data = modificarLamado.num_Ficha
#         formActualizar.nombre_Aprendiz.data = modificarLamado.nombre_Aprendiz
#         formActualizar.num_LlamadosAtencion.data = modificarLamado.num_LlamadosAtencion
#         formActualizar.nombre_Instructor.data = modificarLamado.nombre_Instructor
#         formActualizar.correo_Aprendiz.data = modificarLamado.correo_Aprendiz
#         formActualizar.fecha.data = modificarLamado.fecha
#         formActualizar.falta.data = modificarLamado.falta
#         formActualizar.tipo_Falta.data = modificarLamado.tipo_Falta
#         formActualizar.art_Incumplido.data = modificarLamado.art_Incumplido
#         formActualizar.motivo.data = modificarLamado.motivo
#         formActualizar.plan_Mejora.data = modificarLamado.plan_Mejora
#         formActualizar.firma_Instructor.data = modificarLamado.firma_Instructor
#         formActualizar.firma_Aprendiz.data = modificarLamado.firma_Aprendiz
#         formActualizar.firma_Vocero.data = modificarLamado.firma_Vocero
#     if formActualizar.validate_on_submit() and request.method == "POST":
#         llamadoObj = Llamado(
#             num_Ficha = formActualizar.num_Ficha.data,
#             nombre_Aprendiz = formActualizar.nombre_Aprendiz.data,
#             correo_Aprendiz =  formActualizar.correo_Aprendiz.data,
#             num_LlamadosAtencion = formActualizar.num_LlamadosAtencion.data,
#             nombre_Instructor = formActualizar.nombre_Instructor.data,
#             fecha = formActualizar.fecha.data,
#             falta = formActualizar.falta.data,
#             tipo_Falta= formActualizar.tipo_Falta.data,
#             art_Incumplido = formActualizar.art_Incumplido.data,
#             motivo = formActualizar.motivo.data,
#             plan_Mejora = formActualizar.plan_Mejora.data.read(),
#             firma_Instructor = formActualizar.firma_Instructor.data.read(),
#             firma_Aprendiz = formActualizar.firma_Aprendiz.data.read(),
#             firma_Vocero = formActualizar.firma_Vocero.data.read()
#         )
#         LlamadosService.actualizar_llamado(llamadoObj)
#         return "Llamado actualizado"
#     return render_template("modificarLlamado.html", formActualizar = formActualizar, llamado = llamadoObj) 

