from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# Project root folder (stroke-risk-app)
BASE_DIR = Path(__file__).resolve().parent.parent


def create_app():
    # Explicitly tell Flask where templates and static are located
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "main.login"
    login_manager.login_message_category = "warning"

    # Register routes blueprint
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Create database and default admin
    from .models import User

    with app.app_context():
        db.create_all()

        # Default admin user
        if not User.query.first():
            admin = User(username="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

    return app
