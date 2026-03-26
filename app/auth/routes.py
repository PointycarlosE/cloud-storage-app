# app/auth/routes.py
import os
import secrets
from flask import render_template, redirect, url_for, request, flash, Blueprint, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

from app.auth.models import User
from app.config import ADMIN_USERNAME, IS_FIRST_RUN, CONFIGURADO, ROOT_DIR, PASTA_BASE

auth_bp = Blueprint('auth', __name__)

# Dicionário para controlar tentativas de login
login_attempts = {}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login com proteção contra força bruta"""
    if current_user.is_authenticated:
        return redirect(url_for('file.explorar'))
    
    # Verificar tentativas de login
    client_ip = request.remote_addr
    if client_ip in login_attempts:
        attempts, last_attempt = login_attempts[client_ip]
        if attempts >= 5 and datetime.now() - last_attempt < timedelta(minutes=15):
            flash('Muitas tentativas de login. Aguarde 15 minutos.', 'error')
            return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False) == 'on'
        
        user = User.get(username)
        
        if user and user.check_password(password):
            login_attempts.pop(client_ip, None)
            login_user(user, remember=remember, duration=timedelta(days=30 if remember else 1))
            next_page = request.args.get('next', url_for('file.explorar'))
            return redirect(next_page)
        else:
            if client_ip not in login_attempts:
                login_attempts[client_ip] = [1, datetime.now()]
            else:
                login_attempts[client_ip][0] += 1
                login_attempts[client_ip][1] = datetime.now()
            flash('Usuário ou senha inválidos', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    from app.config import IS_FIRST_RUN, CONFIGURADO, ROOT_DIR
    
    # Se já está configurado, redirecionar para login
    if CONFIGURADO and not IS_FIRST_RUN:
        flash('Sistema já configurado. Faça login.', 'info')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        repo_path = request.form.get('repo_path', '').strip()
        
        # Validações
        if not username:
            flash('Digite um nome de usuário', 'error')
            return render_template('setup.html')
        
        if not password:
            flash('Digite uma senha', 'error')
            return render_template('setup.html')
        
        if password != confirm:
            flash('As senhas não coincidem', 'error')
            return render_template('setup.html')
        
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres', 'error')
            return render_template('setup.html')
        
        if not repo_path:
            flash('Digite o caminho da pasta do repositório', 'error')
            return render_template('setup.html')
        
        try:
            password_hash = generate_password_hash(password)
            repo_path_salvo = repo_path
            
            print(f"📁 Caminho digitado: {repo_path}")
            print(f"📁 Caminho salvo no .env: {repo_path_salvo}")
            
            env_path = os.path.join(ROOT_DIR, 'instance', '.env')
            firstrun_path = os.path.join(ROOT_DIR, 'instance', '.firstrun')
            secret_key = secrets.token_hex(32)
            
            env_content = f"""# Configuração do Meu Drive Pessoal
# NÃO COMPARTILHE ESTE ARQUIVO!

# Chave secreta para sessões
SECRET_KEY={secret_key}

# Credenciais do administrador
ADMIN_USERNAME={username}
ADMIN_PASSWORD_HASH={password_hash}

# Pasta base do repositório (onde os arquivos serão armazenados)
PASTA_BASE={repo_path_salvo}
"""
            
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(env_content)
            
            with open(firstrun_path, 'w', encoding='utf-8') as f:
                f.write("configured")
            
            if not os.path.exists(repo_path_salvo):
                os.makedirs(repo_path_salvo)
                print(f"✅ Pasta do repositório criada: {repo_path_salvo}")
            
            flash('✅ Conta criada com sucesso! Reinicie o servidor para aplicar as configurações.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(f'Erro ao criar conta: {str(e)}', 'error')
            print(f"❌ Erro no setup: {e}")
            import traceback
            traceback.print_exc()
            return render_template('setup.html')
    
    return render_template('setup.html')