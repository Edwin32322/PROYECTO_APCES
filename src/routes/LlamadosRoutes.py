
from src.models import User
from ..services.UserService import UserService
from ..services.AuthService import AuthService
from ..models.Forms import  *
import base64
from flask import Blueprint, render_template, redirect, request, url_for, make_response
from flask_login import login_required, current_user
from ..routes.wrappers.wrappers import decorador_rol_usuario, decorador_estado_usuario
from ..helpers.helpers import generate_password_and_user


#Blueprint para categorizar las rutas del usuario 
calls= Blueprint('calls_blueprint', __name__)

@calls.route("registrarLlamado", methods=["POST", "GET"])
def registrarLlamado():
    formRegistrarLlamado = FormularioRegistrarLlamado()
    if formRegistrarLlamado.validate_on_submit() and request.method == "POST":
        return "hola"
    return render_template("registrarLlamado.html", formRegistrarLlamado = formRegistrarLlamado)
