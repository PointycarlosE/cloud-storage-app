# app/auth/routes.py
import os
import re
import secrets
from flask import (
    render_template, redirect, url_for, request,
    flash, Blueprint, session
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import timedelta
from urllib.parse import urlparse

from app.auth.models import User
from app.config import (
    ADMIN_USERNAME, IS_FIRST_RUN, CONFIGURADO,
    ROOT_DIR, PASTA_BASE, IS_PRODUCTION
)
from app.utils.audit import (
    log_login_ok, log_login_falhou, log_login_bloqueado,
    log_logout, log_setup_concluido
)

auth_bp = Blueprint('auth', __name__)


# ===== VALIDAÇÃO DE SENHA FORTE =====
def validar_senha(senha: str) -> tuple[bool, str]:
    """
    Retorna (True, '') se a senha for forte o suficiente.
    Retorna (False, 'motivo') se não for.
    """
    if len(senha) < 12:
        return False, 'A senha deve ter pelo menos 12 caracteres'
    if not re.search(r'[A-Z]', senha):
        return False, 'A senha deve conter pelo menos uma letra maiúscula'
    if not re.search(r'[a-z]', senha):
        return False, 'A senha deve conter pelo menos uma letra minúscula'
    if not re.search(r'\d', senha):
        return False, 'A senha deve conter pelo menos um número'
    if not re.search(r'[^A-Za-z0-9]', senha):
        return False, 'A senha deve conter pelo menos um caractere especial (!@#$%...)'
    return True, ''


# ===== VALIDAÇÃO DE REDIRECT SEGURO =====
def is_safe_redirect(url: str) -> bool:
    """
    Verifica se a URL de redirecionamento é segura (mesma origem).
    Previne open redirect attacks.
    """
    if not url:
        return False
    parsed = urlparse(url)
    # URL segura: sem scheme e sem netloc (é relativa ao mesmo servidor)
    return not parsed.scheme and not parsed.netloc


# ===== LOGIN =====
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login com rate limiting via flask-limiter (em __init__.py)."""
    if current_user.is_authenticated:
        return redirect(url_for('file.explorar'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        user = User.get(username)

        if user and user.check_password(password):
            log_login_ok(username)

            # "Lembrar-me": 7 dias (reduzido de 30)
            # Sem "lembrar-me": expira com o browser (sessão)
            duration = timedelta(days=7) if remember else None
            login_user(user, remember=remember, duration=duration)

            # Validar redirect antes de usar — previne open redirect
            next_page = request.args.get('next', '')
            if not is_safe_redirect(next_page):
                next_page = url_for('file.explorar')

            return redirect(next_page)
        else:
            log_login_falhou(username)
            # Mensagem genérica — não revela se o usuário existe ou não
            flash('Usuário ou senha inválidos', 'error')

    return render_template('login.html')


# ===== LOGOUT =====
@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    log_logout(username)
    logout_user()
    session.clear()  # Limpa toda a sessão, não só o login
    flash('Você foi desconectado com sucesso', 'success')
    return redirect(url_for('auth.login'))


# ===== SETUP =====
@auth_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    """
    Configuração inicial do sistema.
    Acessível apenas na primeira execução.
    """
    # Reler do disco a cada request — evita problema de estado em memória
    first_run_file = os.path.join(ROOT_DIR, 'instance', '.firstrun')
    ja_configurado = (
        os.path.exists(first_run_file)
        and bool(os.environ.get('ADMIN_USERNAME'))
        and bool(os.environ.get('ADMIN_PASSWORD_HASH'))
        and bool(os.environ.get('PASTA_BASE'))
    )

    if ja_configurado:
        flash('Sistema já configurado. Faça login.', 'info')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        nome = request.form.get('nome', '').strip() or username
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        repo_path = request.form.get('repo_path', '').strip()

        # --- Validações ---
        if not username or len(username) < 3:
            flash('O nome de usuário deve ter pelo menos 3 caracteres', 'error')
            return render_template('setup.html')

        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            flash('O nome de usuário só pode conter letras, números, _ . -', 'error')
            return render_template('setup.html')

        senha_ok, motivo = validar_senha(password)
        if not senha_ok:
            flash(motivo, 'error')
            return render_template('setup.html')

        if password != confirm:
            flash('As senhas não coincidem', 'error')
            return render_template('setup.html')

        if not repo_path:
            flash('Digite o caminho da pasta do repositório', 'error')
            return render_template('setup.html')

        # Normalizar e validar o caminho da pasta
        repo_path = os.path.normpath(repo_path)
        if not os.path.isabs(repo_path):
            flash('O caminho da pasta deve ser absoluto (ex: /storage/emulated/0/MeuDrive)', 'error')
            return render_template('setup.html')

        try:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256:600000')
            secret_key = secrets.token_hex(32)

            env_path = os.path.join(ROOT_DIR, 'instance', '.env')
            firstrun_path = os.path.join(ROOT_DIR, 'instance', '.firstrun')

            env_content = (
                "# Configuração do Cloud Storage App\n"
                "# NÃO COMPARTILHE ESTE ARQUIVO!\n"
                "\n"
                "# Ambiente: development ou production\n"
                "FLASK_ENV=development\n"
                "\n"
                "# Chave secreta para sessões (gerada automaticamente)\n"
                f"SECRET_KEY={secret_key}\n"
                "\n"
                "# Credenciais do administrador\n"
                f"ADMIN_USERNAME={username}\n"
                f"ADMIN_NOME={nome}\n"
                f"ADMIN_PASSWORD_HASH={password_hash}\n"
                "\n"
                "# Pasta base do repositório\n"
                f"PASTA_BASE={repo_path}\n"
                "\n"
                "# Limites (opcional — valores padrão comentados)\n"
                "# MAX_UPLOAD_MB=500\n"
                "# MAX_ZIP_FILES=100\n"
                "# MAX_ZIP_SIZE_MB=1024\n"
                "# PORT=5000\n"
            )

            os.makedirs(os.path.dirname(env_path), exist_ok=True)

            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(env_content)

            with open(firstrun_path, 'w', encoding='utf-8') as f:
                f.write("configured")

            if not os.path.exists(repo_path):
                os.makedirs(repo_path, exist_ok=True)

            log_setup_concluido(username)
            flash('✅ Conta criada com sucesso! Reinicie o servidor e faça login.', 'success')
            return redirect(url_for('auth.login'))

        except PermissionError:
            flash('Sem permissão para criar a pasta ou o arquivo de configuração', 'error')
        except Exception:
            # Não expor detalhes do erro
            flash('Erro ao salvar configuração. Verifique o caminho da pasta.', 'error')

    return render_template('setup.html')