# auth/routes.py
from flask import render_template, redirect, url_for, request, flash, Blueprint, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from auth.models import User
from config import ADMIN_USERNAME

auth_bp = Blueprint('auth', __name__)

# Dicionário para controlar tentativas de login (em produção, use Redis ou banco)
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
        
        user = User.get(username)
        
        if user and user.check_password(password):
            # Login bem-sucedido - limpar tentativas
            login_attempts.pop(client_ip, None)
            
            login_user(user, remember=True, duration=timedelta(days=7))
            next_page = request.args.get('next', url_for('file.explorar'))
            return redirect(next_page)
        else:
            # Registrar tentativa falha
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