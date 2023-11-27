from src.models.SolicitarCita import solicitarCitacion
from src.models.Citacion import Citacion
from ..models.Email import Email as Correo
from datetime import datetime
from flask import jsonify, abort
from ..services.CitacionesService import CitacionesService
from ..services.CasosAprendizService import CasosAprendizService
from ..services.LlamadosService import LlamadosService
from ..models.Forms import  *
import base64
from io import BytesIO
from flask import Blueprint, jsonify,render_template, redirect, request, url_for, make_response, send_file
from flask_login import login_required, current_user
from ..routes.wrappers.wrappers import decorador_rol_usuario, decorador_estado_usuario

#Blueprint para categorizar las rutas del usuario 
citacion = Blueprint('citacion_blueprint', __name__)

@citacion.route("/solicitarCitacion", methods=["POST", "GET"])
@login_required
@decorador_rol_usuario("Instructor")
def solicitudCita():
    formSolicitarCita = FormularioSolicitarCitacion()
    if formSolicitarCita.validate_on_submit() and request.method == "POST":
        solicitar = solicitarCitacion(
            None,
            num_Ficha = request.form["num_Ficha"],
            nombre_Aprendiz = request.form["nombre_Aprendiz"],
            correo_Aprendiz = request.form["correo_Aprendiz"],
            llamados = request.files["llamados"].read(), 
        )
        
        CitacionesService.solicitar_citacion(solicitar)
        
        return "Hola"

    return render_template("solicitarCitacion.html", formSolicitarCita = formSolicitarCita)

@citacion.route("/visualizarSolicitudes", methods=["POST", "GET"])
@login_required
@decorador_rol_usuario("Administrador")
def visualizarSolicitudes():
    llamados = LlamadosService.consultarLlamados()
    return render_template("visualizarLlamados.html", llamados = llamados)

@citacion.route("/aprendiz/enviarCitacionAprendiz", methods=["POST", "GET"])
@login_required
@decorador_rol_usuario("Administrador")
def enviarCitacion():
    formCitacion = FormularioEnviarCitacion()
    formCitacion.citacion_Aprendiz.choices = rellenar_choices_campo_citaciones()
    if formCitacion.validate_on_submit():
        print("hola")
        print(formCitacion.aprendiz.data)
        hora_formateada = formCitacion.hora.data.strftime('%I:%M %p')
        return f"{hora_formateada}"
    return render_template("enviarCitacionAprendiz.html", formEnviarCitacion = formCitacion)


def rellenar_choices_campo_citaciones():
    citaciones = CitacionesService.consultar_citaciones_registradas()
    array = [((None,"Seleccione una citacion"))]
    if citaciones:
        for citacion in citaciones:
            array.append(((citacion.id_Citacion, citacion.fecha_Citacion)))
    return array

@citacion.route("/participantes/enviarCitacionParticipantes", methods=["POST", "GET"])
@login_required
@decorador_rol_usuario("Administrador")
def enviarCitacionParticipantesComite():
    formCitacionParticipantes = FormularioEnviarCitacionParticipantes()
    
    if formCitacionParticipantes.validate_on_submit():
        if request.method == "POST":
            citacion = Citacion(
                id_Citacion = None,
                fecha_Citacion = formCitacionParticipantes.fecha.data,
                hora_Citacion = formCitacionParticipantes.hora.data.strftime('%I:%M %p'),
                correo_Citacion = formCitacionParticipantes.correo_Participantes.data,
                asunto_Citacion = formCitacionParticipantes.asunto.data,
                descripcion_Citacion = formCitacionParticipantes.descripcion.data
                 
            )
            if (not CitacionesService.consultar_existencia_citacion(citacion)):
                if (not CitacionesService.consultar_existencia_citacion_rango(citacion.fecha_Citacion)):
                    CitacionesService.crear_citacion(citacion)
                    Correo().enviar_citacion_participantes(citacion)
                    return "Citacion Registrada con éxito"
                else:
                    return "Ya existen una citacion en un rango de 30 dias"
    return render_template("enviarCitacionParticipantes.html", formEnviarCitacionParticipantes = formCitacionParticipantes)




@citacion.route('/visualizarCitaciones')
@login_required
@decorador_rol_usuario("Administrador")
def visualizarCitaciones():
    citaciones = CitacionesService.consultar_todas_las_citaciones()
    return render_template("visualizarCitaciones.html", citaciones = citaciones)









@citacion.route('/aprendiz/obtenerDatosAprendiz/<int:id_Caso>')
@login_required
@decorador_rol_usuario("Administrador")
def obtenerAprendicesParaCitar(id_Caso):
    caso =  CasosAprendizService.consultar_caso_por_id(id_Caso)
    if caso:
        detalles_aprendiz = {"nombre": caso.correo_Aprendiz, "otro_campo": caso.correo_Aprendiz}
        return jsonify(detalles_aprendiz)
    else:
        return jsonify({})
    


@citacion.route('/aprendiz/obtenerDatosCitaciones/<int:id_Citacion>')
@login_required
@decorador_rol_usuario("Administrador")
def obtenerCitacionesParaAprendiz(id_Citacion):
    citacion = CitacionesService.consultar_citacion(id_Citacion)
    
    if citacion:
        hora_formateada = datetime.strptime(citacion.hora_Citacion, "%I:%M %p").strftime('%H:%M')
        detalles_citacion = {"fecha": citacion.fecha_Citacion, "hora": hora_formateada}
        return jsonify(detalles_citacion)
    else:
        abort(404)



