
from ..services.AuthService import AuthService
from ..services.UserService import UserService
from ..helpers.helpers import generate_password
from ..models.Forms import FormUser
from flask import Blueprint, jsonify, render_template, redirect, request, flash, url_for, current_app
from flask_login import login_user, logout_user, current_user

from ..app import login_manager
from ..models.User import User
from ..models.Email import Email

from itsdangerous import SignatureExpired, BadSignature

#Creamos un blueprint encargado de manejar las rutas de autenticación
main = Blueprint('auth_blueprint', __name__)


#Es importante definirlo debido que este decorador es el que recupera el objeto usuario de la sesion en cada solicitud
@login_manager.user_loader
def load_User(id):
    return AuthService.get_by_id(id)


@main.route('/', methods=['GET', 'POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('users_blueprint.zonaPrincipal'))
    
    formUser = FormUser()
    if formUser.validate_on_submit():
        if request.method == 'POST':
            #Construimos un objeto usuario con los valores proporcionados
            user = User(correo_Usuario=formUser.correo_Usuario.data, contrasena_Usuario=formUser.contrasena_Usuario.data)
            #Enviamos dicho objeto al class method para usarlo en la validacion con la base de datos
            logged_User = AuthService.login_user(user)
            
            #Si lo que devolvió del llamado al método no está vacío
            if logged_User is not None:
                
                
                #Si el campo de contrasena_Usuario del objeto que nos devolvió el método es True quiere decir que las credenciales son válidas
                if logged_User.contrasena_Usuario:
                    #Si el usuario está inhabilitado
                    if logged_User.estado_Usuario ==  0:
                        flash('Usuario inhabilitado', 'usuario_inhabilitado')
                        return render_template('login.html', formUser = formUser)
            
                    
                    #Si todo sale bien, guardamos al usuario en la sesión
                    
                    login_user(logged_User)
                    
                    #Redireccionamos al usuario al blueprint que contiene la vista de zona principal (home)
                    
                    return redirect(url_for('users_blueprint.zonaPrincipal'))
                else:
                    
                    flash('Contraseña incorrecta')
            else:
                flash('Usuario no encontrado')
    #Enviamos el objeto formulario para que este renderize los campos con sus respectivas validaciones
    return render_template('login.html', formUser = formUser)


@main.route('/recuperarContraseña', methods = ['GET','POST'])
def recuperar_contra():
    
    if current_user.is_authenticated:
        return redirect(url_for('users_blueprint.zonaPrincipal'))
    
    if request.method == 'POST':
        correo = request.form['correo_Usuario']
        usuario = AuthService.get_by_email(correo)
        if usuario is not None:
            email = Email()
            usuario_receptor = email.enviar_correo_recuperar_contrasena(correo)
            if usuario_receptor:
                flash(message="Se ha enviado a su correo las instrucciones para el cambio de contraseña")
                return redirect(url_for('auth_blueprint.login'))
        else:
            flash(message='No existe ningún usuario con ese correo', category="correo_recuperar_contraseña")
            return redirect(url_for('auth_blueprint.recuperar_contra'))
    else:
        return render_template('recuperarContra.html')

@main.route('/recuperarContraseña/<int:id>/<string:token>', methods = ['GET', 'POST'])
def comprobar_validez_token(id, token):
    if current_user.is_authenticated:
        return redirect(url_for('users_blueprint.zonaPrincipal'))
    try:
        current_app.config["SERIALIZER"].loads(token, max_age=3600)
    except SignatureExpired:
        # El token ha expirado
        return "El enlace ha expirado"
    except BadSignature:
    # El token es inválido
        return "El enlace no es válido"
    return render_template("cambiarContra.html", id = id)

@main.route('/recuperarContraseña/cambiar/<id>', methods =['POST'])
def cambiar_contraseña(id):
    if current_user.is_authenticated:
        return redirect(url_for('users_blueprint.zonaPrincipal'))
    
    contrasena = request.form['nueva_Contraseña']
    confimarcion_contrasena = request.form['confirmacion_Contraseña']
    if contrasena == confimarcion_contrasena:
        usuario = User(id_Usuario=id, contrasena_Usuario=generate_password(contrasena))
        actualizacion_contra = UserService.cambiar_contra(usuario)
        if actualizacion_contra:
            return redirect(url_for('auth_blueprint.login'))
        else:
            return "No se ha podido realizar la actualización"
    else:
        return "Las contraseñas no son iguales"


#Ruta para cerra la sesión del usuario
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))




#Funciones encargadas de manejar los estados de protocolo de transferencia
def status_401(exc):
    return redirect(url_for('auth_blueprint.login'))

def status_404(exc):
    error = jsonify({
        'error' : 'Not Found',
        'message' : 'La página que deseas buscar no existe o no se encuentra'
    })
    return error
