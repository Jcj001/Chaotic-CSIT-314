from flask import Flask
from .entity import db
from .boundary import boundary


def init_app():
    app = Flask(__name__)

    # APPLICATION CONFIGURATIONS
    app.config['SECRET_KEY'] = "12345678"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

    # BLUEPRINTS REGISTRATION
    app.register_blueprint(boundary)

    # INITIALIZING DATABASE
    db.init_app(app)
    with app.app_context():
        import application.entity.models
        db.create_all()

    return app
