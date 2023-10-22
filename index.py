from config import config
from src import init_app, csrf
#Almacenamos la configuración en una variale
configuracion = config['development']
#Invocamos el método que nos devolverá de regreso la app, pero configurda, enviandole la configuracion proveniente de la clase
app = init_app(configuracion)

#Si este modulo 'index.py' es ejecutado de forma principal, arrancará la aplicación
if __name__  == '__main__':
    csrf.init_app(app)
    app.run(port=5900)