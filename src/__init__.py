
from .routes import AuthRoutes, UserRoutes, LlamadosRoutes, CasosAprendizRoutes, SolicitarCitacionRoutes
from .routes.AuthRoutes import status_401, status_404
from .app import app, csrf

#Función que configura la app por medio de un objeto, con los blueprints con su determinado préfijo, los status not found y unauthorized.
def init_app(config):
    app.config.from_object(config)
    app.register_blueprint(AuthRoutes.main, url_prefix='/')
    app.register_blueprint(UserRoutes.users, url_prefix='/usuario')
    app.register_blueprint(LlamadosRoutes.calls, url_prefix='/llamados')
    app.register_blueprint(CasosAprendizRoutes.casos, url_prefix='/casos')
    app.register_blueprint(SolicitarCitacionRoutes.citacion, url_prefix='/citacion')
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    #Retornamos la app con las anteriores configuraciones
    return app
