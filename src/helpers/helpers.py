import secrets
import string
from werkzeug.security import generate_password_hash, check_password_hash

#Helpers auxiliares (Funciones auxiliaress)


#Función para generar los datos de nombre_Usuario y contrasena_Usuario de forma aleatoria
def generate_password_and_user():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    usuario = ''
    contrasena = ''
    for a in range(0, 10):
        usuario += secrets.choice(caracteres)
        contrasena += secrets.choice(caracteres)
    return {
            'usuario' : usuario, 
            'contrasena' : contrasena
            }
    
#Funcion para comprobrar el hash guardado en la base de datos, con la contraseña ingresada por el usuario en la vista
def check_password(hashed_Password, contrasena_Usuario):
    return check_password_hash(hashed_Password, contrasena_Usuario)


#Funcion para generar el hash de una contraseña
def generate_password(password):
    return generate_password_hash(password, salt_length=8)
    