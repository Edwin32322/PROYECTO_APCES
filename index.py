from config import config
from src import init_app, csrf
from celery import Celery
#Almacenamos la configuración en una variale
configuracion = config['development']
#Invocamos el método que nos devolverá de regreso la app, pero configurda, enviandole la configuracion proveniente de la clase
app = init_app(configuracion)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
#Si este modulo 'index.py' es ejecutado de forma principal, arrancará la aplicación
if __name__  == '__main__':
    celery = make_celery(app)
    csrf.init_app(app)
    app.run(port=5900)