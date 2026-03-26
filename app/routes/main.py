# app/routes/main.py
from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user
from app.auth.decorators import login_required_optional
from app.config import CONFIGURADO, IS_FIRST_RUN

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Rota principal - redireciona para o lugar correto baseado no estado do sistema"""
    # Se não está configurado, vai para setup
    if not CONFIGURADO or IS_FIRST_RUN:
        return redirect(url_for('auth.setup'))
    
    # Se já está logado, vai para explorador
    if current_user.is_authenticated:
        return redirect(url_for('file.explorar'))
    
    # Se não está logado, vai para login
    return redirect(url_for('auth.login'))

@main_bp.route('/objetivos')
@login_required_optional
def objetivos():
    return render_template('objetivos.html')