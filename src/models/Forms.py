
#Validación de formularios por medio de Flask-WTF

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, EmailField, IntegerField, SelectField, FileField

from wtforms.validators import DataRequired, Email


#Clase que valida los campos del login 
class FormUser(FlaskForm):
    correo_Usuario = EmailField('correo_Usuario', validators=[
        DataRequired(message='El campo del correo debe ser diligenciado'),
        Email(message="El correo no es correcto")
    ])
    contrasena_Usuario = StringField('contrasena_Usuario', validators=[
        DataRequired(message='El campo de la contraseña debe ser diligenciado')
    ]
    )
    submit = SubmitField('enviar')
    
class FormPasswordRecover(FlaskForm):
    correo_Usuario = EmailField('correo_Usuario', validators=[
        DataRequired(message="Este campo es obligatorio")
    ])
    submit = SubmitField('Enviar')
        
#Clase encargada de validar los campos en la vista de Registrar Usuario
class UserRegister(FlaskForm):
    numero_Documento_Usuario = StringField('numero_Documento_Usuario')
    tipoDoc_Usuario = SelectField('tipoDoc_Usuario', choices=[
        ('Cédula de Ciudadanía'), ('Cédula de extranjería'), ('PEP')
    ])
    correo_Usuario = EmailField('correo_Usuario', validators=[
        Email(message='El correo no es correcto')
    ])
    nombre_Usuario = StringField('nombre_Usuario', validators=[
        DataRequired(message='El campo del nombre de usuario no puede estar vacío')
    ])
    contrasena_Usuario = StringField('contraseña_Usuario', render_kw={'readonly' : False})
    id_Rol_FK = SelectField('rol_Usuario', choices=[
        (1, 'Administrador'), (2, 'Instructor')
    ], validators=[
        DataRequired(message='Este campo es obligatorio')
    ])
    submit = SubmitField('Registrar')
    
    
class UserProfile(FlaskForm):
    numero_Documento_Usuario = StringField('numero_Documento_Usuario', validators=[
        DataRequired('El campo es obligatorio')
    ])
    tipoDoc_Usuario = SelectField('tipoDoc_Usuario', choices=[
        ('Cédula de Ciudadanía'), ('Cédula de extranjería'), ('PEP')
    ])
    telefono_Usuario = IntegerField('telefono_Usuario', validators=[
        DataRequired('El campo es obligatorio')
    ])
    correo_Usuario = correo_Usuario = EmailField('correo_Usuario', validators=[
        DataRequired(message='El campo del correo debe ser diligenciado'),
        Email(message="El correo no es correcto")
    ])
    nombre_Usuario = StringField('nombre_Usuario', validators=[
        DataRequired(message='El campo del nombre de usuario no puede estar vacío')
    ])
    estado_Usuario =  SelectField('rol_Usuario', choices=[
        (1, 'Activo'), (0, 'Inactivo')
    ], validators=[
        DataRequired(message='Este campo es obligatorio')
    ])
    id_Rol_FK = SelectField('rol_Usuario', choices=[
        (1, 'Administrador'), (2, 'Instructor')
    ], validators=[
        DataRequired(message='Este campo es obligatorio')
    ])