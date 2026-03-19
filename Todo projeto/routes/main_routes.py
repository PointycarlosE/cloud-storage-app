# routes/main_routes.py
from flask import render_template
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/objetivos')
def objetivos():
    return render_template('objetivos.html')