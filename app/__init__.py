# app/__init__.py
from flask import Flask
from flask_login import LoginManager
import os

from app.config import (
    PASTA_BASE, DEBUG, HOST, PORT, SECRET_KEY, 
    REQUIRE_LOGIN, CONFIGURADO, IS_FIRST_RUN, ROOT_DIR
)
from app.auth.models import User
from app.auth.routes import auth_bp
from app.routes.main import main_bp
from app.routes.files import file_bp

# Criar aplicação Flask
app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

# Configurações
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Registrar Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(file_bp)
app.register_blueprint(auth_bp)

# Context processor global
@app.context_processor
def inject_globals():
    return {
        'PASTA_BASE': PASTA_BASE,
        'IS_FIRST_RUN': IS_FIRST_RUN,
        'CONFIGURADO': CONFIGURADO
    }