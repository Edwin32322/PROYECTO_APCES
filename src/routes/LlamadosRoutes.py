
from src.models.Llamado import Llamado
from ..services.LlamadosService import LlamadosService
from ..models.Forms import  *
import base64
from io import BytesIO
from flask import Blueprint, render_template, redirect, request, url_for, make_response, send_file
from flask_login import login_required, current_user
from ..routes.wrappers.wrappers import decorador_rol_usuario, decorador_estado_usuario
from ..helpers.helpers import generate_password_and_user


#Blueprint para categorizar las rutas del usuario 
calls= Blueprint('calls_blueprint', __name__)

@calls.route("registrarLlamado", methods=["POST", "GET"])
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
        plan_Mejora_base64 = base64.b64encode(llamado.plan_Mejora).decode('utf-8')
        llamado.plan_Mejora_base64 = 'data:application/pdf;base64,' + plan_Mejora_base64
        
        
        return render_template("visualizarLlamado.html", llamado = llamado)

    return render_template("registrarLlamado.html", formRegistrarLlamado = formRegistrarLlamado)

@calls.route("visualizarLlamados")
def visualizarLlamados():
    llamados = LlamadosService.consultarLlamados()
    return f"{llamados}"

