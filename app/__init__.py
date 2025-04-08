from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "young thug city"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:pass@db:5432/appdb"
    migrate = Migrate(app, db)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from auth.routes import bp

        app.register_blueprint(bp)

    return app
