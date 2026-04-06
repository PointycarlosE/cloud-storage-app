# app/__init__.py
from flask import Flask, jsonify, render_template, request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

from app.config import (
    PASTA_BASE, DEBUG, SECRET_KEY,
    REQUIRE_LOGIN, CONFIGURADO, IS_FIRST_RUN, ROOT_DIR,
    SESSION_COOKIE_SECURE, SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SAMESITE,
    PERMANENT_SESSION_LIFETIME, MAX_CONTENT_LENGTH, IS_PRODUCTION,
    RATELIMIT_DEFAULT
)
from app.auth.models import User
from app.auth.routes import auth_bp
from app.routes.main import main_bp
from app.routes.files import file_bp

# ===== CRIAR APLICAÇÃO =====
app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

# ===== CONFIGURAÇÕES =====
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Sessão
app.config['SESSION_COOKIE_SECURE'] = SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = SESSION_COOKIE_SAMESITE
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME

# CSRF — necessário para flask-wtf
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # token CSRF expira em 1 hora

# ===== CSRF PROTECTION =====
csrf = CSRFProtect(app)

# ===== RATE LIMITING =====
# Armazena contadores em memória (para Termux sem Redis)
# Para produção com múltiplos workers, use storage_uri="redis://localhost:6379"
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[RATELIMIT_DEFAULT],
    storage_uri="memory://",
)

# ===== FLASK-LOGIN =====
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# ===== REGISTRAR BLUEPRINTS =====
app.register_blueprint(main_bp)
app.register_blueprint(file_bp)
app.register_blueprint(auth_bp)

# Exportar limiter para uso nos blueprints
app.limiter = limiter

# ===== HEADERS DE SEGURANÇA HTTP =====
@app.after_request
def aplicar_headers_seguranca(response):
    """
    Adiciona headers de segurança em todas as respostas.
    Esses headers são a primeira linha de defesa no navegador.
    """
    # Impede que a página seja carregada em iframes (clickjacking)
    response.headers['X-Frame-Options'] = 'DENY'

    # Impede que o browser "adivinhe" o tipo do arquivo (MIME sniffing)
    response.headers['X-Content-Type-Options'] = 'nosniff'

    # Habilita proteção XSS do browser (legacy, mas útil)
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # Em produção com HTTPS: força HTTPS por 1 ano, incluindo subdomínios
    if IS_PRODUCTION:
        response.headers['Strict-Transport-Security'] = (
            'max-age=31536000; includeSubDomains'
        )

    # Política de referrer: não vaza URL ao navegar para outros sites
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    # Content Security Policy básica:
    # - default: só recursos do próprio servidor
    # - style/script: próprio servidor + inline (necessário para o JS atual)
    # - img: qualquer origem (para preview de imagens)
    # Ajuste conforme seu frontend evoluir
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "media-src 'self'; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )

    # Remove header que revela que é Flask/Werkzeug
    response.headers.pop('Server', None)
    response.headers.pop('X-Powered-By', None)

    return response

# ===== TRATAMENTO DE ERROS =====
@app.errorhandler(400)
def bad_request(e):
    if request.is_json or request.path.startswith('/deletar_multiplos'):
        return jsonify(erro="Requisição inválida"), 400
    return render_template('erro.html', mensagem="Requisição inválida."), 400

@app.errorhandler(403)
def forbidden(e):
    if request.is_json:
        return jsonify(erro="Acesso negado"), 403
    return render_template('erro.html', mensagem="Acesso negado."), 403

@app.errorhandler(404)
def not_found(e):
    if request.is_json:
        return jsonify(erro="Não encontrado"), 404
    return render_template('erro.html', mensagem="Página não encontrada."), 404

@app.errorhandler(413)
def request_too_large(e):
    from app.config import MAX_UPLOAD_SIZE_MB
    if request.is_json:
        return jsonify(erro=f"Arquivo muito grande. Limite: {MAX_UPLOAD_SIZE_MB}MB"), 413
    return render_template(
        'erro.html',
        mensagem=f"Arquivo muito grande. O limite é {MAX_UPLOAD_SIZE_MB}MB."
    ), 413

@app.errorhandler(429)
def too_many_requests(e):
    if request.is_json:
        return jsonify(erro="Muitas requisições. Aguarde um momento."), 429
    return render_template('erro.html', mensagem="Muitas requisições. Aguarde um momento."), 429

@app.errorhandler(CSRFError)
def csrf_error(e):
    if request.is_json:
        return jsonify(erro="Token de segurança inválido. Recarregue a página."), 400
    return render_template(
        'erro.html',
        mensagem="Token de segurança inválido. Por favor, recarregue a página e tente novamente."
    ), 400

@app.errorhandler(500)
def internal_error(e):
    # NUNCA expor detalhes do erro em produção
    if IS_PRODUCTION:
        msg = "Erro interno do servidor."
    else:
        msg = f"Erro interno: {str(e)}"
    if request.is_json:
        return jsonify(erro=msg), 500
    return render_template('erro.html', mensagem=msg), 500

# ===== CONTEXT PROCESSOR =====
@app.context_processor
def inject_globals():
    return {
        'PASTA_BASE': PASTA_BASE,
        'IS_FIRST_RUN': IS_FIRST_RUN,
        'CONFIGURADO': CONFIGURADO,
        'IS_PRODUCTION': IS_PRODUCTION,
    }