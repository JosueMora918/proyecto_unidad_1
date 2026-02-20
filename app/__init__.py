from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect  # <--- IMPORTANTE: Importar esto

db = SQLAlchemy()
csrf = CSRFProtect()  # <--- IMPORTANTE: Crear instancia


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    csrf.init_app(app)  # <--- IMPORTANTE: Iniciar la protección en la app

    # Importar y registrar Blueprints
    from .routes.user_routes import user_bp
    from .routes.auth_routes import auth_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app