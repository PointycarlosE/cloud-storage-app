# app/config.py
import os
import secrets
from dotenv import load_dotenv

# ENCONTRAR O CAMINHO DA RAIZ DO PROJETO (subindo um nível)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, 'instance', '.env')
FIRST_RUN_FILE = os.path.join(ROOT_DIR, 'instance', '.firstrun')


# CARREGAR .env
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH, override=True)
    print(f"✅ .env carregado de: {ENV_PATH}")

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

# Segurança
REQUIRE_LOGIN = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = 86400

# ===== CONTROLE DE PRIMEIRA EXECUÇÃO =====
CONFIGURADO = os.path.exists(FIRST_RUN_FILE) and ADMIN_USERNAME and ADMIN_PASSWORD_HASH and PASTA_BASE
IS_FIRST_RUN = not CONFIGURADO

if IS_FIRST_RUN:
    print("🆕 PRIMEIRA EXECUÇÃO DETECTADA!")
else:
    print("✅ Configurações carregadas com sucesso!")
    print(f"📁 Pasta base: {PASTA_BASE}")
    print(f"👤 Usuário: {ADMIN_USERNAME}")