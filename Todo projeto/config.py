# config.py
import os
import secrets
from dotenv import load_dotenv

print("Carregando config.py...")
print("ADMIN_USERNAME do .env:", os.environ.get('ADMIN_USERNAME'))

# CARREGAR .env ANTES DE TUDO
load_dotenv()

# Defina a pasta base corretamente
PASTA_BASE = os.path.abspath("C:/Users/cacae/REPOSITORIO")

# Configurações do Flask
DEBUG = True  # Em produção, mude para False
HOST = '0.0.0.0'
PORT = 5000

# ===== CONFIGURAÇÕES DE AUTENTICAÇÃO =====
# Chave secreta (usa variável de ambiente, ou gera uma aleatória)
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Credenciais do usuário (OBRIGATÓRIO vir do .env)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')

# Segurança
REQUIRE_LOGIN = True
SESSION_COOKIE_SECURE = False  # Mude para True quando usar HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = 86400  # 24 horas

# Verificar se as credenciais estão configuradas
if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
    print("❌ ERRO: Credenciais não configuradas no arquivo .env!")
    print("O arquivo .env deve conter:")
    print("ADMIN_USERNAME=admin")
    print("ADMIN_PASSWORD_HASH=pbkdf2:sha256:260000$...")
    print("")
    print("Use este comando para gerar um hash:")
    print('python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash(\'admin123\'))"')
    raise ValueError("Credenciais não configuradas no arquivo .env!")

print("✅ Configurações carregadas com sucesso!")