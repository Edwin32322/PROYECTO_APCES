
from ..services.UserService import UserService
from ..services.AuthService import AuthService
from ..app import app
from ..models.Forms import  *
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from ..routes.wrappers.wrappers import decorador_rol_usuario, decorador_estado_usuario
from ..helpers.helpers import generate_password_and_user
from ..models.User import User


#Blueprint para categorizar las rutas del usuario 
users= Blueprint('users_blueprint', __name__)

#Ruta de la zona principal
@users.route('/zonaPrincipal')
@login_required
@decorador_estado_usuario()
def zonaPrincipal():
    return render_template('zonaPrincipal.html')

#Ruta para visualizar usuarios
@users.route('/visualizarUsuarios')
@login_required
@decorador_estado_usuario()
def visualizarUsuarios():
    users = UserService.obtener_usuarios()
    return render_template('visualizarUsuarios.html', users = users)

#Ruta para visualizar al usuario
@users.route('/visualizarUsuario/<int:id>')
@login_required
@decorador_estado_usuario()
def verUsuario(id):
    user = AuthService.get_by_id(id)
    return render_template('visualizarUsuario.html', user = user)


#Ruta que renderiza la vista para modificar el estado del usuario
@users.route('/modificarEstado/<int:id>', methods=['POST'])
@login_required
@decorador_rol_usuario('Administrador')
@decorador_estado_usuario()
def modificarEstado(id):
    return render_template('modificarEstadoUsuario.html', id = id)

#Ruta para modifcar el estado
@users.route('/modificarEstado/<string:opcion>/<int:id>')
@login_required
@decorador_rol_usuario('Administrador')
@decorador_estado_usuario()
def modificarEstadoUsuario(opcion, id):
    user = AuthService.get_by_id(id)
    if UserService.modificar_estado_usuario(user, opcion):
        return redirect(url_for('users_blueprint.verUsuario', id = id ))
    return redirect(url_for('users_blueprint.verUsuario', id = id))

#Ruta para registrar un usuario
@users.route('/registrarUsuario', methods=['GET', 'POST'])
@login_required
@decorador_rol_usuario('Administrador')
@decorador_estado_usuario()
def registrarUsuario():
    form_user_register = UserRegister()
    datos_random_usuario = generate_password_and_user()
    if form_user_register.validate_on_submit():
        if request.method == 'POST':
            user = User(
            None,
            request.form['numero_Documento_Usuario'],
            request.form['tipoDoc_Usuario'],
            None,
            request.form['correo_Usuario'],
            request.form['nombre_Usuario'],
            request.form['contrasena_Usuario'],
            None,
            True,
            request.form['id_Rol_FK']
            )
            if UserService.checkear_email_en_bd(user):
                UserService.registrar_usuario(user)
                return render_template('registrarUsuario.html', form_user_register = form_user_register, datos_usuario_registrado = user, datos_usuario = datos_random_usuario,message_exito = 'Usuario registrado con éxito')
            else:
                return render_template('registrarUsuario.html', form_user_register = form_user_register, datos_usuario = datos_random_usuario, message_err = 'Ya existe un usuario con ese correo')
    return render_template('registrarUsuario.html', form_user_register = form_user_register, datos_usuario = datos_random_usuario)

@users.route('/verPerfil/<int:id>')
def verPerfil(id):
    userProfile = UserProfile()
    if id == current_user.id_Usuario:
        userProfile.id_Usuario = current_user.id_Usuario
        userProfile.tipoDoc_Usuario.data = current_user.tipoDoc_Usuario
        userProfile.numero_Documento_Usuario.data = current_user.numero_Documento_Usuario
        userProfile.telefono_Usuario.data = current_user.telefono_Usuario
        userProfile.correo_Usuario.data = current_user.correo_Usuario
        userProfile.nombre_Usuario.data = current_user.nombre_Usuario
        userProfile.estado_Usuario.data = current_user.estado_Usuario
        userProfile.id_Rol_FK.data = current_user.id_Rol_FK
    else:
        user = AuthService.get_by_id(id)
        userProfile.id_Usuario = user.id_Usuario
        userProfile.tipoDoc_Usuario.data = user.tipoDoc_Usuario
        userProfile.numero_Documento_Usuario.data = user.numero_Documento_Usuario
        userProfile.telefono_Usuario.data = user.telefono_Usuario
        userProfile.correo_Usuario.data = user.correo_Usuario
        userProfile.nombre_Usuario.data = user.nombre_Usuario
        userProfile.estado_Usuario.data = user.estado_Usuario
        userProfile.id_Rol_FK.data = user.id_Rol_FK
    return render_template('perfilUsuario.html', userProfile = userProfile)

@users.route('/modificarUsuario/<int:id>', methods=['POST'])
def modificarUsuario(id):
    userProfile = UserProfile()
    if userProfile.validate_on_submit():
        # imagen = request.files['imagen_Usuario']
        # imagen_cargada = imagen.read()
        user = User(
            id_Usuario= id,
            numero_Documento_Usuario= userProfile.numero_Documento_Usuario.data,
            tipoDoc_Usuario= userProfile.tipoDoc_Usuario.data,
            telefono_Usuario= userProfile.telefono_Usuario.data,
            correo_Usuario= userProfile.correo_Usuario.data,
            nombre_Usuario= userProfile.nombre_Usuario.data,
            estado_Usuario= userProfile.estado_Usuario.data,
            id_Rol_FK= userProfile.id_Rol_FK.data
        )
        if UserService.actualizar_usuario(user):
            return redirect(url_for('users_blueprint.verUsuario', id = user.id_Usuario))
        else:
            print("Hubo un error")
    
    return redirect(url_for('users_blueprint.verPerfil', id = id))

@users.route('/actualizarImagen/<int:id>', methods=["POST"])
def actualizar_imagen(id):
    if request.method == 'POST':
        if 'nueva-imagen' in request.files:
            nueva_imagen = request.files['nueva-imagen']
            if nueva_imagen.filename != '':
                imagen_cargada = nueva_imagen.read()
                user = User(id_Usuario=id, imagen_Usuario=imagen_cargada)
                UserService.cambiar_imagen_usuario(user)
                return redirect(url_for('users_blueprint.verUsuario', id=id))
    
    return redirect(url_for('users_blueprint.verUsuario', id=id))

@users.route('/imagen/<int:id>')
def serve_image(id):
    user = AuthService.get_by_id(id)
    imagen =  user.imagen_Usuario
    if imagen is not None:
        return app.response_class(imagen, mimetype='image/jpg')
    else:
        return '¡Imagen no encontrada!', 404
