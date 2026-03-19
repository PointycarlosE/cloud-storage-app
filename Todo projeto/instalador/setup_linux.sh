#!/bin/bash

# Cores
VERDE='\033[0;32m'
AMARELO='\033[1;33m'
AZUL='\033[0;34m'
VERMELHO='\033[0;31m'
RESET='\033[0m'

echo -e "${AZUL}==================================================${RESET}"
echo -e "${AZUL}   📁 MEU DRIVE PESSOAL - INSTALADOR AUTOMÁTICO${RESET}"
echo -e "${AZUL}==================================================${RESET}"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${VERMELHO}[ERRO] Python 3 não encontrado!${RESET}"
    echo ""
    echo "Por favor, instale o Python 3.8 ou superior:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  MacOS: brew install python3"
    echo ""
    exit 1
fi

echo -e "${VERDE}[OK] Python 3 encontrado${RESET}"
echo ""

# Verificar Git
if ! command -v git &> /dev/null; then
    echo -e "${AMARELO}[AVISO] Git não encontrado. Vamos baixar o ZIP.${RESET}"
    USAR_GIT=0
    # Verificar se wget ou curl existe
    if ! command -v wget &> /dev/null && ! command -v curl &> /dev/null; then
        echo -e "${VERMELHO}[ERRO] Nem wget nem curl encontrados. Instale um deles:${RESET}"
        echo "  Ubuntu/Debian: sudo apt install wget"
        echo "  Fedora: sudo dnf install wget"
        exit 1
    fi
else
    echo -e "${VERDE}[OK] Git encontrado${RESET}"
    USAR_GIT=1
fi
echo ""

# Perguntar onde instalar
echo -e "${AZUL}Digite o caminho onde deseja instalar o Meu Drive Pessoal${RESET}"
echo -e "${AZUL}(ou pressione ENTER para instalar em $HOME/MeuDrivePessoal):${RESET}"
read -r PASTA_INSTALACAO

if [ -z "$PASTA_INSTALACAO" ]; then
    PASTA_INSTALACAO="$HOME/MeuDrivePessoal"
fi

echo -e "${VERDE}Instalando em: $PASTA_INSTALACAO${RESET}"
echo ""

# Criar pasta de instalação
mkdir -p "$PASTA_INSTALACAO"
cd "$PASTA_INSTALACAO" || exit

# Baixar o projeto
echo -e "${AZUL}[1/6] Baixando projeto do GitHub...${RESET}"
if [ "$USAR_GIT" -eq 1 ]; then
    git clone https://github.com/PointycarlosE/Servidor-Python.git temp
else
    echo "Baixando via ZIP..."
    if command -v wget &> /dev/null; then
        wget -O temp.zip https://github.com/PointycarlosE/Servidor-Python/archive/refs/heads/main.zip
    else
        curl -L -o temp.zip https://github.com/PointycarlosE/Servidor-Python/archive/refs/heads/main.zip
    fi
    unzip temp.zip -d temp
    rm temp.zip
fi

# IDENTIFICAR A PASTA CORRETA DO PROJETO
echo "Verificando estrutura de pastas..."

if [ -d "$PASTA_INSTALACAO/temp/Servidor-Python-main" ]; then
    echo "Encontrada pasta: Servidor-Python-main"
    PASTA_ORIGEM="$PASTA_INSTALACAO/temp/Servidor-Python-main"
elif [ -d "$PASTA_INSTALACAO/temp/Todo projeto" ]; then
    echo "Encontrada pasta: Todo projeto"
    PASTA_ORIGEM="$PASTA_INSTALACAO/temp/Todo projeto"
elif [ -d "$PASTA_INSTALACAO/temp/Todo Projeto" ]; then
    echo "Encontrada pasta: Todo Projeto"
    PASTA_ORIGEM="$PASTA_INSTALACAO/temp/Todo Projeto"
else
    echo "Usando pasta temp diretamente"
    PASTA_ORIGEM="$PASTA_INSTALACAO/temp"
fi

# Copiar arquivos
echo "Copiando arquivos para $PASTA_INSTALACAO..."
cp -rf "$PASTA_ORIGEM/." "$PASTA_INSTALACAO/" 2>/dev/null

# Limpar temp
rm -rf "$PASTA_INSTALACAO/temp"

echo -e "${VERDE}[OK] Projeto baixado${RESET}"
echo ""

# DETERMINAR ONDE ESTÁ O CONFIG.PY
if [ -f "$PASTA_INSTALACAO/config.py" ]; then
    PASTA_CONFIG="$PASTA_INSTALACAO"
    echo "Config encontrado na raiz"
elif [ -f "$PASTA_INSTALACAO/Todo projeto/config.py" ]; then
    PASTA_CONFIG="$PASTA_INSTALACAO/Todo projeto"
    echo "Config encontrado em Todo projeto"
elif [ -f "$PASTA_INSTALACAO/Todo Projeto/config.py" ]; then
    PASTA_CONFIG="$PASTA_INSTALACAO/Todo Projeto"
    echo "Config encontrado em Todo Projeto"
elif [ -f "$PASTA_INSTALACAO/Servidor-Python-main/config.py" ]; then
    PASTA_CONFIG="$PASTA_INSTALACAO/Servidor-Python-main"
    echo "Config encontrado em Servidor-Python-main"
else
    PASTA_CONFIG="$PASTA_INSTALACAO"
    echo "Usando raiz como pasta de configuracao"
fi

CONFIG_PATH="$PASTA_CONFIG/config.py"
echo "Config path: $CONFIG_PATH"
echo ""

# Perguntar pasta do repositório
echo -e "${AZUL}[2/6] Configuração da pasta de repositório${RESET}"
echo -e "Digite o caminho da pasta que você deseja usar como repositório de arquivos"
echo -e "(ex: /home/usuario/MeusArquivos, /media/HD/Documentos, etc)"
echo -e "Ou pressione ENTER para usar a pasta padrão: $HOME/MeuDriveRepositorio"
echo ""

read -r PASTA_REPOSITORIO
if [ -z "$PASTA_REPOSITORIO" ]; then
    PASTA_REPOSITORIO="$HOME/MeuDriveRepositorio"
fi

# Criar pasta do repositório
mkdir -p "$PASTA_REPOSITORIO"
echo -e "${VERDE}[OK] Pasta do repositório: $PASTA_REPOSITORIO${RESET}"
echo ""

# Configurar config.py
echo -e "${AZUL}[3/6] Configurando arquivos...${RESET}"

# Usar sed para substituir a linha da PASTA_BASE
sed -i "s|PASTA_BASE = os.path.abspath.*|PASTA_BASE = os.path.abspath(\"$PASTA_REPOSITORIO\")|g" "$CONFIG_PATH"

echo -e "${VERDE}[OK] Configuração concluída${RESET}"
echo ""

# Criar ambiente virtual
echo -e "${AZUL}[4/6] Criando ambiente virtual...${RESET}"
cd "$PASTA_CONFIG"

# Remover venv antigo se existir
if [ -d "venv" ]; then
    echo "Removendo ambiente virtual antigo..."
    rm -rf venv
fi

# Criar novo ambiente virtual
python3 -m venv venv

if [ ! -f "venv/bin/activate" ]; then
    echo -e "${VERMELHO}[ERRO] Falha ao criar ambiente virtual!${RESET}"
    exit 1
fi

echo -e "${VERDE}[OK] Ambiente virtual criado${RESET}"
echo ""

# Instalar dependências
echo -e "${AZUL}[5/6] Instalando dependências...${RESET}"
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Verificar se requirements.txt existe
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt não encontrado. Instalando Flask diretamente..."
    pip install flask
fi

# Verificar se Flask foi instalado
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${AMARELO}[AVISO] Flask não instalado. Tentando novamente...${RESET}"
    pip install flask
else
    echo -e "${VERDE}[OK] Flask instalado com sucesso${RESET}"
fi

deactivate
echo -e "${VERDE}[OK] Dependências instaladas${RESET}"
echo ""

# PROCURAR O SCRIPT DE INICIALIZAÇÃO
echo -e "${AZUL}[6/6] Configurando atalhos...${RESET}"

SCRIPT_INICIAR=""
if [ -f "$PASTA_CONFIG/iniciar.sh" ]; then
    SCRIPT_INICIAR="$PASTA_CONFIG/iniciar.sh"
    echo "Script de inicialização encontrado na raiz"
elif [ -f "$PASTA_CONFIG/Todo projeto/iniciar.sh" ]; then
    SCRIPT_INICIAR="$PASTA_CONFIG/Todo projeto/iniciar.sh"
    echo "Script encontrado em Todo projeto"
elif [ -f "$PASTA_CONFIG/Todo Projeto/iniciar.sh" ]; then
    SCRIPT_INICIAR="$PASTA_CONFIG/Todo Projeto/iniciar.sh"
    echo "Script encontrado em Todo Projeto"
elif [ -f "$PASTA_CONFIG/Servidor-Python-main/iniciar.sh" ]; then
    SCRIPT_INICIAR="$PASTA_CONFIG/Servidor-Python-main/iniciar.sh"
    echo "Script encontrado em Servidor-Python-main"
fi

# Dar permissão de execução ao script
if [ -n "$SCRIPT_INICIAR" ]; then
    chmod +x "$SCRIPT_INICIAR"
    echo -e "${VERDE}[OK] Permissão de execução concedida ao script${RESET}"
else
    echo -e "${AMARELO}[AVISO] Script de inicialização não encontrado${RESET}"
fi

# Perguntar sobre atalhos
echo ""
echo -e "${AZUL}Deseja criar um atalho na área de trabalho para iniciar o servidor? (s/N)${RESET}"
read -r CRIAR_ATALHO

# Criar atalho na área de trabalho se o usuário quiser
if [[ "$CRIAR_ATALHO" =~ ^[Ss]$ ]] && [ -n "$SCRIPT_INICIAR" ]; then
    DESKTOP="$HOME/Desktop"
    if [ -d "$DESKTOP" ]; then
        # Criar arquivo .desktop
        cat > "$DESKTOP/MeuDrivePessoal.desktop" << EOF
[Desktop Entry]
Name=Meu Drive Pessoal
Comment=Iniciar servidor Meu Drive Pessoal
Exec=$SCRIPT_INICIAR
Icon=$PASTA_CONFIG/static/img/favicon.ico
Terminal=true
Type=Application
Categories=Network;
EOF
        chmod +x "$DESKTOP/MeuDrivePessoal.desktop"
        echo -e "${VERDE}[OK] Atalho criado na área de trabalho: $DESKTOP/MeuDrivePessoal.desktop${RESET}"
    else
        echo -e "${AMARELO}[AVISO] Pasta Desktop não encontrada em $DESKTOP${RESET}"
        echo "Criando atalho na pasta do usuário..."
        
        # Alternativa: criar na home
        cat > "$HOME/MeuDrivePessoal.desktop" << EOF
[Desktop Entry]
Name=Meu Drive Pessoal
Comment=Iniciar servidor Meu Drive Pessoal
Exec=$SCRIPT_INICIAR
Icon=$PASTA_CONFIG/static/img/favicon.ico
Terminal=true
Type=Application
Categories=Network;
EOF
        chmod +x "$HOME/MeuDrivePessoal.desktop"
        echo -e "${VERDE}[OK] Atalho criado em: $HOME/MeuDrivePessoal.desktop${RESET}"
    fi
fi

echo -e "${VERDE}[OK] Configuração de atalhos concluída${RESET}"
echo ""

# OBTER IP DA MÁQUINA
IP=$(hostname -I | awk '{print $1}')

# Mostrar relatório final
echo -e "${AZUL}==================================================${RESET}"
echo -e "${VERDE}   ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!${RESET}"
echo -e "${AZUL}==================================================${RESET}"
echo ""
echo -e "${AZUL}📁 Projeto instalado em:${RESET} $PASTA_CONFIG"
echo -e "${AZUL}📁 Repositório de arquivos:${RESET} $PASTA_REPOSITORIO"
echo ""
echo -e "${AZUL}🚀 Para iniciar o servidor:${RESET}"
if [ -n "$SCRIPT_INICIAR" ]; then
    echo "   $SCRIPT_INICIAR"
else
    echo "   cd $PASTA_CONFIG && source venv/bin/activate && python3 app.py"
fi

if [[ "$CRIAR_ATALHO" =~ ^[Ss]$ ]] && [ -f "$DESKTOP/MeuDrivePessoal.desktop" ]; then
    echo "   • Atalho na área de trabalho"
fi
echo ""
echo -e "${AZUL}🌐 Para acessar:${RESET}"
echo "   • Local: http://localhost:5000"
echo "   • Rede:  http://$IP:5000"
echo ""

# Perguntar sobre iniciar agora
echo -e "${AZUL}Deseja iniciar o servidor agora? (s/N)${RESET}"
read -r INICIAR_AGORA

# Iniciar servidor se o usuário quiser
if [[ "$INICIAR_AGORA" =~ ^[Ss]$ ]]; then
    echo -e "${AZUL}Iniciando servidor...${RESET}"
    
    if [ -n "$SCRIPT_INICIAR" ] && [ -f "$SCRIPT_INICIAR" ]; then
        echo "Executando: $SCRIPT_INICIAR"
        
        # Detectar ambiente gráfico e abrir terminal apropriado
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "$SCRIPT_INICIAR; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "$SCRIPT_INICIAR" &
        elif command -v konsole &> /dev/null; then
            konsole -e "$SCRIPT_INICIAR" &
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            osascript -e "tell application \"Terminal\" to do script \"$SCRIPT_INICIAR\""
        else
            # Fallback: iniciar em background
            cd "$PASTA_CONFIG"
            source venv/bin/activate
            python3 app.py &
        fi
        
        # Aguardar 3 segundos
        sleep 3
        
        # Abrir navegador
        if command -v xdg-open &> /dev/null; then
            xdg-open "http://localhost:5000" 2>/dev/null
        elif command -v open &> /dev/null; then
            open "http://localhost:5000" 2>/dev/null
        fi
        
        echo -e "${VERDE}Servidor iniciado!${RESET}"
    else
        echo -e "${VERMELHO}[ERRO] Script de inicialização não encontrado!${RESET}"
    fi
fi

echo ""
echo "Pressione ENTER para sair..."
read -r