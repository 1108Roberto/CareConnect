from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="young thug in 2012",
        SQLALCHEMY_DATABASE_URI="postgresql://user:pass@db:5432/appdb",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import main
    from app.auth import bp as auth_bp
    from app.patient import bp as patient_bp

    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)

    # Simple route for testing
    @app.route("/test")
    def test_route():
        return "Works!"

    return app
