from flask import Flask
# Importar cualquier otra extensión que necesites


def create_app():
    app = Flask(__name__)

    # Configurar la aplicación
    # app.config['ALGUNA_CONFIGURACION'] = 'valor'

    # Inicializar extensiones
    # db.init_app(app)
    # migrate.init_app(app, db)

    # Registrar blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Aquí podrías añadir cualquier otra inicialización que necesites

    return app
