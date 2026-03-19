# app.py
from flask import Flask
from config import PASTA_BASE, DEBUG, HOST, PORT
from routes.main_routes import main_bp
from routes.file_routes import file_bp

# Criar aplicação Flask
app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(file_bp)

# Disponibilizar PASTA_BASE para os templates (opcional)
@app.context_processor
def inject_globals():
    return {'PASTA_BASE': PASTA_BASE}

if __name__ == '__main__':
    print(f"🚀 Servidor rodando em http://{HOST}:{PORT}")
    print(f"📁 Pasta base: {PASTA_BASE}")
    app.run(host=HOST, port=PORT, debug=DEBUG)