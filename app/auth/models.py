# app/auth/models.py
from werkzeug.security import check_password_hash
import os

class User:
    """Modelo de usuário seguro"""
    
    def __init__(self, username, password_hash=None):
        self.username = username
        self.password_hash = password_hash
        self._is_authenticated = True
        self._is_active = True
        self._is_anonymous = False
    
    def get_id(self):
        return self.username
    
    def check_password(self, password):
        """Verifica se a senha está correta usando hash"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get(username):
        """Busca usuário pelo nome"""
        # CORRIGIR: ler do ambiente diretamente (não precisa de import)
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH', '')
        
        if username == admin_username:
            return User(admin_username, admin_password_hash)
        return None
    
    @property
    def is_authenticated(self):
        return self._is_authenticated
    
    @is_authenticated.setter
    def is_authenticated(self, value):
        self._is_authenticated = value
    
    @property
    def is_active(self):
        return self._is_active
    
    @is_active.setter
    def is_active(self, value):
        self._is_active = value
    
    @property
    def is_anonymous(self):
        return self._is_anonymous
    
    @is_anonymous.setter
    def is_anonymous(self, value):
        self._is_anonymous = value