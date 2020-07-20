from flask import Flask
from flask_mail import Mail
from .config import Config
from flask_login import LoginManager


mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message = ""


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    login_manager.init_app(app)

    from .models import db
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app



    
    