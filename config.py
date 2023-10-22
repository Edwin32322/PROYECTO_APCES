# La librería decouple me permite trabajar con las variables de entorno de forma flexible (permite modularizar 
# y separar las configuración de la aplicación de forma segura para no incluirla directamente en el código fuente)

#Podemos definir dichas variables en el archivo .env

from decouple import config
from itsdangerous import URLSafeTimedSerializer
#Clase que contiene la secret key
class Config():
    SECRET_KEY = config('SECRET_KEY')
    SERIALIZER = URLSafeTimedSerializer(config('SECRET_KEY'))

#Clase que hereda la secret key de la clase config y activa el modo Debug
class DevelopmentConfig(Config):
    DEBUG = True

#Encapsulamos la clase en un una variable config que se usará después en index.py
config = {
    'development': DevelopmentConfig
}
