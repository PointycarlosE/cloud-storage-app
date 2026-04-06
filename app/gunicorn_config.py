# gunicorn_config.py
import multiprocessing
import os

# ===== REDE =====
# Escuta em todas as interfaces na porta 5000
# No Termux, use 0.0.0.0 para permitir acesso via Wi-Fi local
bind = "0.0.0.0:5000"

# ===== WORKERS =====
# No Termux (celulares antigos), muitos workers podem travar o sistema.
# Recomendado para Termux: 2 ou 3 workers no máximo.
workers = 2

# Tipo de worker (sync é o mais estável para Android/Termux)
worker_class = 'sync'

# Tempo máximo de execução de uma requisição (segundos)
# Aumentado para suportar uploads grandes e downloads em ZIP
timeout = 300

# ===== SEGURANÇA =====
# Limita o tamanho do corpo da requisição (500MB conforme config.py)
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Previne vazamento de informações do servidor
server = "CloudStorageApp/1.0"

# ===== LOGS =====
# Logs de acesso e erro (podem ser redirecionados para arquivos no Termux)
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"

# ===== PROXY REVERSO =====
# Necessário se usar Cloudflare Tunnel ou Nginx na frente
forwarded_allow_ips = '*'
proxy_allow_ips = '*'
