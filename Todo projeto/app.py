# app.py
from flask import Flask
from flask_login import LoginManager

from config import PASTA_BASE, DEBUG, HOST, PORT, SECRET_KEY
from routes.main_routes import main_bp
from routes.file_routes import file_bp
from auth.routes import auth_bp
from auth.models import User
from dotenv import load_dotenv
load_dotenv()

# Criar aplicação Flask
app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = SECRET_KEY

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Carrega usuário pelo ID para o Flask-Login"""
    return User.get(user_id)

# Registrar Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(file_bp)
app.register_blueprint(auth_bp)

# Disponibilizar PASTA_BASE para os templates (opcional)
@app.context_processor
def inject_globals():
    return {'PASTA_BASE': PASTA_BASE}

if __name__ == '__main__':
    print(f"🚀 Servidor rodando em http://{HOST}:{PORT}")
    print(f"📁 Pasta base: {PASTA_BASE}")
    app.run(host=HOST, port=PORT, debug=DEBUG)