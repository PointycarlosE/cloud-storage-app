# app/config.py
import os
import secrets
from dotenv import load_dotenv

# ===== CAMINHOS =====
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, 'instance', '.env')
FIRST_RUN_FILE = os.path.join(ROOT_DIR, 'instance', '.firstrun')

# ===== CARREGAR .env =====
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH, override=True)

# ===== AMBIENTE =====
# Para ativar produção: defina FLASK_ENV=production no .env ou no ambiente
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
IS_PRODUCTION = FLASK_ENV == 'production'

# DEBUG nunca ativo em produção — independente do que estiver no .env
DEBUG = False if IS_PRODUCTION else os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'

# ===== REDE =====
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))

# ===== SEGURANÇA DE SESSÃO =====
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    # Se não há SECRET_Key no .env, gera uma temporária e avisa
    SECRET_KEY = secrets.token_hex(32)
    if IS_PRODUCTION:
        # Em produção sem SECRET_KEY definida, isso é um erro grave
        raise RuntimeError(
            "SECRET_KEY não definida no .env! "
            "Execute: python -c \"import secrets; print(secrets.token_hex(32))\" "
            "e adicione ao .env como SECRET_KEY=<valor>"
        )

# Cookies de sessão
# Em produção (HTTPS obrigatório): Secure=True impede envio em HTTP
SESSION_COOKIE_SECURE = IS_PRODUCTION
SESSION_COOKIE_HTTPONLY = True          # Bloqueia acesso via JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'        # Proteção CSRF básica em nível de cookie

# Tempo de sessão padrão (sem "lembrar-me"): 8 horas
PERMANENT_SESSION_LIFETIME = 8 * 60 * 60  # segundos

# ===== CREDENCIAIS =====
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_NOME = os.environ.get('ADMIN_NOME', ADMIN_USERNAME)
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')
PASTA_BASE = os.environ.get('PASTA_BASE')

# ===== AUTENTICAÇÃO =====
REQUIRE_LOGIN = True  # Nunca desativar em produção

# ===== CONTROLE DE PRIMEIRA EXECUÇÃO =====
CONFIGURADO = (
    os.path.exists(FIRST_RUN_FILE)
    and bool(ADMIN_USERNAME)
    and bool(ADMIN_PASSWORD_HASH)
    and bool(PASTA_BASE)
)
IS_FIRST_RUN = not CONFIGURADO

# ===== LIMITES DE UPLOAD =====
MAX_UPLOAD_SIZE_MB = int(os.environ.get('MAX_UPLOAD_MB', 500))
MAX_CONTENT_LENGTH = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# ===== LIMITES DO ZIP =====
MAX_ZIP_FILES = int(os.environ.get('MAX_ZIP_FILES', 100))       # máx arquivos por ZIP
MAX_ZIP_SIZE_MB = int(os.environ.get('MAX_ZIP_SIZE_MB', 1024))  # máx 1GB por ZIP

# ===== RATE LIMITING =====
# Quantas requisições por minuto por IP em rotas normais
RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '60 per minute')
# Limite específico para login (mais restritivo)
RATELIMIT_LOGIN = os.environ.get('RATELIMIT_LOGIN', '10 per minute')

# ===== LOG DE AUDITORIA =====
AUDIT_LOG_PATH = os.path.join(ROOT_DIR, 'instance', 'audit.log')
AUDIT_LOG_MAX_MB = int(os.environ.get('AUDIT_LOG_MAX_MB', 10))  # rotação a cada 10MB

# ===== FEEDBACK NO TERMINAL (apenas informativo, sem dados sensíveis) =====
if IS_FIRST_RUN:
    print("🆕 PRIMEIRA EXECUÇÃO — acesse /setup para configurar")
else:
    env_label = "🔴 PRODUÇÃO" if IS_PRODUCTION else "🟡 DESENVOLVIMENTO"
    print(f"{env_label} | Debug: {DEBUG} | Porta: {PORT}")
    print(f"📁 Pasta base: {PASTA_BASE}")
    print(f"👤 Usuário: {ADMIN_USERNAME}")
    if not IS_PRODUCTION:
        print("⚠️  Para ativar modo produção: defina FLASK_ENV=production no .env")