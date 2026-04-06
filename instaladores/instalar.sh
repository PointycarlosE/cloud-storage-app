#!/bin/bash

# Cores para o terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}    INSTALADOR - CLOUD STORAGE APP        ${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# 1. Verificar se é Termux
IS_TERMUX=false
if [[ -d "/data/data/com.termux" ]]; then
    IS_TERMUX=true
    echo -e "${BLUE}[INFO] Ambiente Termux detectado.${NC}"
fi

# 2. Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERRO] Python 3 não encontrado!${NC}"
    if [ "$IS_TERMUX" = true ]; then
        echo "Execute: pkg install python"
    else
        echo "Por favor, instale o Python 3.8+."
    fi
    exit 1
fi

# 3. Criar Ambiente Virtual (VENV)
echo -e "${BLUE}[1/4] Criando ambiente virtual (venv)...${NC}"
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERRO] Falha ao criar venv. Verifique se python3-venv está instalado.${NC}"
    if [ "$IS_TERMUX" = false ]; then
        echo "Tente: sudo apt install python3-venv"
    fi
    exit 1
fi

# 4. Instalar Dependências
echo -e "${BLUE}[2/4] Instalando dependências (isso pode demorar)...${NC}"
source venv/bin/activate
pip install --upgrade pip > /dev/null
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERRO] Falha ao instalar dependências. Verifique sua internet.${NC}"
    exit 1
fi

# 5. Configurar .env inicial
echo -e "${BLUE}[3/4] Configurando variáveis de ambiente...${NC}"
mkdir -p instance
if [ ! -f instance/.env ]; then
    cat <<EOT > instance/.env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=524288000
EOT
    echo -e "${GREEN}[OK] Arquivo .env criado com chave secreta aleatória.${NC}"
fi

# 6. Criar Script de Inicialização Rápida
echo -e "${BLUE}[4/4] Criando script de inicialização rápida...${NC}"
cat <<EOT > iniciar.sh
#!/bin/bash
source venv/bin/activate
python3 run.py
EOT
chmod +x iniciar.sh

if [ "$IS_TERMUX" = true ]; then
    echo -e "${GREEN}[OK] Script 'iniciar.sh' criado!${NC}"
    echo "Para rodar o servidor no Termux, use: ./iniciar.sh"
else
    # Tenta criar atalho .desktop no Linux Desktop
    if [ -d "$HOME/.local/share/applications" ]; then
        cat <<EOT > "$HOME/.local/share/applications/cloud-storage.desktop"
[Desktop Entry]
Name=Cloud Storage App
Exec=$(pwd)/iniciar.sh
Icon=folder-remote
Type=Application
Terminal=true
Categories=Utility;
EOT
        echo -e "${GREEN}[OK] Atalho criado no menu de aplicativos!${NC}"
    fi
fi

echo ""
echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}    INSTALAÇÃO CONCLUÍDA COM SUCESSO!     ${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""
echo "Para iniciar o servidor, execute: ./iniciar.sh"
echo ""
