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
actas= Blueprint('acta_blueprint', __name__)

@actas.route("/generarActa", methods=["GET", "POST"])
def generarActa():
    formActa = FormularioGenerarActa()
    if formActa.validate_on_submit():
        return "valido"
    return render_template("generarActa.html", formActa = formActa)