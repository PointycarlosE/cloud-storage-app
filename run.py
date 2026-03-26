# run.py
from app import app

if __name__ == '__main__':
    from app.config import HOST, PORT, DEBUG, IS_FIRST_RUN
    
    if IS_FIRST_RUN:
        print("🆕 Primeira execução detectada!")
        print("   Acesse http://localhost:5000/setup para configurar")
    else:
        print(f"🚀 Servidor rodando em http://{HOST}:{PORT}")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)