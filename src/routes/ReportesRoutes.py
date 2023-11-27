from docx2pdf import convert
from ..models.Email import Email as Correo
import tempfile
import pythoncom
from src.models.Llamado import Llamado
from src.services.CasosAprendizService import CasosAprendizService
from src.uploads.ModificarArchivos import covertir_a_pdf
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

#Blueprint para categorizar las rutas de reportes
reportes = Blueprint('reportes_blueprint', __name__)

@reportes.route("/visualizarReportes/llamados")
@login_required
@decorador_estado_usuario()
def visualizarReportesLlamados():
    llamados = LlamadosService.consultarLlamados()
    return render_template("visualizarLlamados.html", llamados = llamados)

@reportes.route("/visualizarReportes/citaciones")
@login_required
@decorador_estado_usuario()
def visualizarReportesCitaciones():
    llamados = LlamadosService.consultarLlamados()
    return render_template("visualizarLlamados.html", llamados = llamados)


@reportes.route("/visualizarReportes/actas")
@login_required
@decorador_estado_usuario()
def visualizarReportesActas():
    llamados = LlamadosService.consultarLlamados()
    return render_template("visualizarLlamados.html", llamados = llamados)
