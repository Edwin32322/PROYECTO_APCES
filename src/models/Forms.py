
#Validación de formularios por medio de Flask-WTF

from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField,EmailField,IntegerField, SelectField, FileField, DateField, PasswordField

from wtforms.validators import DataRequired, Email, NumberRange, ValidationError
from flask_wtf.file import FileAllowed, FileRequired

def longitud_campo_integer_field(form, field):
    min_length = 5  
    max_length = 15  
    valorString = str(field.data)
    if valorString is not None and not (min_length <= len(valorString) <= max_length):
        raise validators.ValidationError('El número debe estar entre {} y {} dígitos.'.format(min_length, max_length))

#Clase que valida los campos del login 
class FormUser(FlaskForm):
    correo_Usuario = EmailField('correo_Usuario', validators=[
        DataRequired(message='El campo del correo debe ser diligenciado'),
        Email(message="El correo no es correcto")
    ])
    contrasena_Usuario = PasswordField('contrasena_Usuario', validators=[
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
    numero_Documento_Usuario = IntegerField('numero_Documento_Usuario', validators=[
        DataRequired("El campo es requerido"),
        longitud_campo_integer_field
    ])
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
    numero_Documento_Usuario = IntegerField('numero_Documento_Usuario', render_kw={'readonly' : True}, validators=[
        DataRequired('El campo es obligatorio y debe ser númerico'),
        longitud_campo_integer_field,
        NumberRange(min=0, message='El campo debe ser un número positivo')
    ])
    tipoDoc_Usuario = SelectField('tipoDoc_Usuario', choices=[
        ('Cédula de Ciudadanía'), ('Cédula de extranjería'), ('PEP')
    ])
    telefono_Usuario = IntegerField('telefono_Usuario', validators=[
        DataRequired('El campo es obligatorio y debe ser númerico'),
        longitud_campo_integer_field,
        NumberRange(min=0, message='El campo debe ser un número positivo')
    ])
    correo_Usuario = correo_Usuario = EmailField('correo_Usuario', render_kw={'readonly' : True},validators=[
        DataRequired(message='El campo del correo debe ser diligenciado'),
        Email(message="El correo no es correcto")
    ])
    nombre_Usuario = StringField('nombre_Usuario', validators=[
        DataRequired(message='El campo del nombre de usuario no puede estar vacío')
    ])
    estado_Usuario =  SelectField('rol_Usuario', render_kw={'readonly' : True},choices=[
        (1, 'Activo'), (0, 'Inactivo')
    ], validators=[
        DataRequired(message='Este campo es obligatorio')
    ])

class FormularioRegistrarLlamado(FlaskForm):
    num_Ficha = IntegerField("num_Ficha", validators=[
        DataRequired('El campo es obligatorio y debe ser númerico'),
        longitud_campo_integer_field,
        NumberRange(min=0, message='El campo debe ser un número positivo')
    ])
    nombre_Aprendiz = StringField("nombre_Aprendiz", validators=[
        DataRequired("El campo es requerido")
    ])
    correo_Aprendiz = EmailField("correo_Aprendiz", validators=[
        DataRequired("El campo es requerido"),
        Email(message="El correo no es correcto")
        
    ])
    num_LlamadosAtencion = IntegerField("num_LlamadosAtencion", validators=[
        DataRequired('El campo es obligatorio y debe ser númerico'),
        NumberRange(min=0, message='El campo debe ser un número positivo')
    ])
    nombre_Instructor = StringField("nombre_Instructor", validators=[
        DataRequired("El campo es requerido")
    ])
    fecha = DateField(validators=[
        DataRequired(message="El campo es obligatorio")
    ])
    falta = SelectField("falta", choices=[
        (1, "Grave"), (2, "Moderada"), (3, "Leve")
    ])
    tipo_Falta = SelectField("falta", choices=[
        (1, "Grave"), (2, "Moderada"), (3, "Leve")
    ])
    art_Incumplido = SelectField("falta", choices=[
        (1, "Grave"), (2, "Moderada"), (3, "Leve")
    ])
    motivo = StringField("motivo", validators=[
        DataRequired("El campo es requerido")
    ])
    plan_Mejora = FileField("plan_Mejora", validators=[
        DataRequired("El campo es requerido"),
        FileAllowed(["pdf"], "Solo se admiten extensiones PDF"),
        FileRequired("Debe haber un archivo cargado")
    ])
    firma_Instructor = FileField("firma_Instructor", validators=[
        DataRequired("El campo es requerido"),
        FileAllowed(["png", "jpeg", "jpg"], "Solo se admiten extensiones PNG, JPEG O JPG"),
        FileRequired("Debe haber un archivo cargado")
    ])
    firma_Aprendiz = FileField("firma_Aprendiz", validators=[
        DataRequired("El campo es requerido"),
        FileAllowed(["png", "jpeg", "jpg"], "Solo se admiten extensiones PNG, JPEG O JPG"),
    ])
    firma_Vocero = FileField("firma_Vocero", validators=[
        DataRequired("El campo es requerido"),
        FileAllowed(["png", "jpeg", "jpg"], "Solo se admiten extensiones PNG, JPEG O JPG"),
        FileRequired("Debe haber un archivo cargado")
    ])
    submit = SubmitField('Registrar')


class FormularioCrearCasoAprendiz(FlaskForm):

    tipo_Documento = SelectField('tipo_Documento', choices=[
        ('Cédula de Ciudadanía'), ('Cédula de extranjería'), ('PEP')
    ])
    num_Documento = IntegerField('num_Documento', validators=[
        DataRequired('El campo es obligatorio y debe ser númerico'),
        longitud_campo_integer_field,
        NumberRange(min=0, message='El campo debe ser un número positivo')
    ])
    num_Ficha = IntegerField("num_Ficha", validators=[
        DataRequired('El campo es obligatorio y debe ser númerico'),
        longitud_campo_integer_field,
        NumberRange(min=0, message='El campo debe ser un número positivo')
    ])
    nombre_Aprendiz = StringField("nombre_Aprendiz", validators=[
        DataRequired("El campo es requerido")
    ])
    correo_Aprendiz = EmailField("correo_Aprendiz", validators=[
        DataRequired("El campo es requerido"),
        Email(message="El correo no es correcto")
    ])

    submit = SubmitField('Registrar')


class FormularioSolicitarCitacion(FlaskForm):

    num_Ficha = IntegerField("num_Ficha", validators=[
        DataRequired('El campo es obligatorio y debe ser númerico'),
        longitud_campo_integer_field,
        NumberRange(min=0, message='El campo debe ser un número positivo')
    ])
    nombre_Aprendiz = StringField("nombre_Aprendiz", validators=[
        DataRequired("El campo es requerido")
    ])
    correo_Aprendiz = EmailField("correo_Aprendiz", validators=[
        DataRequired("El campo es requerido"),
        Email(message="El correo no es correcto")
    ])
    llamados = FileField("llamados", validators=[
        DataRequired("El campo es requerido"),
        FileAllowed(["pdf"], "Solo se admiten extensiones PDF"),
        FileRequired("Debe haber un archivo cargado")
    ])

    submit = SubmitField('Enviar')
