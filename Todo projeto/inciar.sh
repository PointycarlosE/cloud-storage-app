#!/bin/bash

# Cores
VERDE='\033[0;32m'
AZUL='\033[0;34m'
RESET='\033[0m'

echo -e "${AZUL}==================================================${RESET}"
echo -e "${AZUL}   🚀 INICIANDO MEU DRIVE PESSOAL${RESET}"
echo -e "${AZUL}==================================================${RESET}"
echo ""

# Ir para a pasta do script
cd "$(dirname "$0")"

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo -e "${VERMELHO}[ERRO] Ambiente virtual não encontrado!${RESET}"
    echo "Execute o instalador novamente."
    exit 1
fi

# Ativar ambiente virtual
echo -e "${VERDE}[OK] Ativando ambiente virtual...${RESET}"
source venv/bin/activate

# Verificar se Flask está instalado
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${AMARELO}[AVISO] Flask não encontrado. Instalando...${RESET}"
    pip install flask
fi

# Obter IP
IP=$(hostname -I | awk '{print $1}')

echo ""
echo -e "${VERDE}[OK] Servidor disponível em:${RESET}"
echo "   • Local: http://localhost:5000"
echo "   • Rede:  http://$IP:5000"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo -e "${AZUL}==================================================${RESET}"
echo ""

# Iniciar servidor
python3 app.py