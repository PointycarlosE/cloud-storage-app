# config.py
import os
import secrets
from dotenv import load_dotenv

# ENCONTRAR O CAMINHO DA RAIZ DO PROJETO
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(ROOT_DIR, '.env')
FIRST_RUN_FILE = os.path.join(ROOT_DIR, '.firstrun')

# CARREGAR .env
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH, override=True)
    print(f"✅ .env carregado de: {ENV_PATH}")
else:
    print(f"⚠️ .env não encontrado em: {ENV_PATH}")

# Configurações do Flask
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# ===== CONFIGURAÇÕES DE AUTENTICAÇÃO =====
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Credenciais do usuário
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')
PASTA_BASE = os.environ.get('PASTA_BASE')

# Se PASTA_BASE não estiver definida, tentar usar um padrão
if not PASTA_BASE:
    # Tentar usar a pasta do usuário
    try:
        user_profile = os.environ.get('USERPROFILE', 'C:/Users')
        PASTA_BASE = os.path.join(user_profile, 'MeuDriveRepositorio')
    except:
        PASTA_BASE = 'C:/MeuDriveRepositorio'

# Segurança
REQUIRE_LOGIN = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = 86400

# ===== CONTROLE DE PRIMEIRA EXECUÇÃO =====
CONFIGURADO = os.path.exists(FIRST_RUN_FILE) and ADMIN_USERNAME and ADMIN_PASSWORD_HASH and PASTA_BASE
IS_FIRST_RUN = not CONFIGURADO

# DEBUG: Mostrar o que foi lido
print(f"🔍 DEBUG - PASTA_BASE: {PASTA_BASE}")
print(f"🔍 DEBUG - Existe? {os.path.exists(PASTA_BASE) if PASTA_BASE else 'N/A'}")

if IS_FIRST_RUN:
    print("🆕 PRIMEIRA EXECUÇÃO DETECTADA!")
    print("   O sistema não está configurado.")
    print("   Acesse /setup para criar sua conta.")
else:
    print("✅ Configurações carregadas com sucesso!")
    print(f"📁 Pasta base: {PASTA_BASE}")
    print(f"👤 Usuário: {ADMIN_USERNAME}")