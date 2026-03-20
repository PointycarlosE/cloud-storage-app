# auth/decorators.py
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from config import REQUIRE_LOGIN

def login_required_optional(view_func):
    """
    Decorador que exige login se REQUIRE_LOGIN for True.
    Útil para desenvolvimento.
    """
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if REQUIRE_LOGIN and not current_user.is_authenticated:
            flash('Por favor, faça login para acessar esta página', 'warning')
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return decorated_function