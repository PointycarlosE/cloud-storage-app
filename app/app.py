# app.py
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
import os

# Carregar .env PRIMEIRO
load_dotenv()

# Depois importar config
from config import PASTA_BASE, DEBUG, HOST, PORT, SECRET_KEY, IS_FIRST_RUN, CONFIGURADO
from app.routes.main import main_bp
from app.routes.files import file_bp
from auth.routes import auth_bp
from auth.models import User

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
    return User.get(user_id)

# Rota raiz - redirecionar inteligente
@app.route('/')
def index():
    # Se o sistema não está configurado, vai para setup
    if IS_FIRST_RUN or not CONFIGURADO:
        return redirect(url_for('auth.setup'))
    
    # Se o usuário já está logado, vai para o explorador
    if current_user.is_authenticated:
        return redirect(url_for('file.explorar'))
    
    # Se não está logado, vai para o login
    return redirect(url_for('auth.login'))

# Registrar Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(file_bp)
app.register_blueprint(auth_bp)

# Disponibilizar PASTA_BASE para os templates
@app.context_processor
def inject_globals():
    return {
        'PASTA_BASE': PASTA_BASE,
        'IS_FIRST_RUN': IS_FIRST_RUN,
        'CONFIGURADO': CONFIGURADO
    }

if __name__ == '__main__':
    if IS_FIRST_RUN or not CONFIGURADO:
        print("🆕 Primeira execução detectada!")
        print("   Acesse http://localhost:5000/setup para configurar")
    else:
        print(f"🚀 Servidor rodando em http://{HOST}:{PORT}")
        print(f"📁 Pasta base: {PASTA_BASE}")
        print(f"🔐 Acesse http://localhost:5000/login para entrar")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)