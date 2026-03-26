# app/routes/main.py
from flask import render_template, Blueprint
from app.auth.decorators import login_required_optional

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required_optional
def home():
    return render_template('home.html')

@main_bp.route('/objetivos')
@login_required_optional
def objetivos():
    return render_template('objetivos.html')