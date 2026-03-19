@echo off
title Meu Drive Pessoal - Instalador Automático
color 0A

echo ===================================================
echo    📁 MEU DRIVE PESSOAL - INSTALADOR AUTOMÁTICO
echo ===================================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.8 ou superior em:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Marque a opcao "Add Python to PATH"
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

:: Verificar se Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Git nao encontrado. Vamos baixar o ZIP diretamente.
    set USAR_GIT=0
) else (
    echo [OK] Git encontrado
    set USAR_GIT=1
)
echo.

:: Perguntar onde instalar
echo Digite o caminho onde deseja instalar o Meu Drive Pessoal
echo (ou pressione ENTER para instalar em C:\MeuDrivePessoal):
set /p PASTA_INSTALACAO=

if "%PASTA_INSTALACAO%"=="" set PASTA_INSTALACAO=C:\MeuDrivePessoal

echo.
echo Instalando em: %PASTA_INSTALACAO%
echo.

:: Criar pasta de instalação
if not exist "%PASTA_INSTALACAO%" mkdir "%PASTA_INSTALACAO%"

:: Entrar na pasta
cd /d "%PASTA_INSTALACAO%"

:: Baixar o projeto
echo [1/6] Baixando projeto do GitHub...
if "%USAR_GIT%"=="1" (
    git clone https://github.com/PointycarlosE/Servidor-Python.git temp
) else (
    echo Baixando via ZIP...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/PointycarlosE/Servidor-Python/archive/refs/heads/main.zip' -OutFile 'temp.zip'"
    powershell -Command "Expand-Archive -Path 'temp.zip' -DestinationPath 'temp' -Force"
    del temp.zip
)

:: IDENTIFICAR A PASTA CORRETA DO PROJETO
echo Verificando estrutura de pastas...

if exist "%PASTA_INSTALACAO%\temp\Servidor-Python-main" (
    echo Encontrada pasta: Servidor-Python-main
    set PASTA_ORIGEM=%PASTA_INSTALACAO%\temp\Servidor-Python-main
) else if exist "%PASTA_INSTALACAO%\temp\Todo projeto" (
    echo Encontrada pasta: Todo projeto
    set PASTA_ORIGEM=%PASTA_INSTALACAO%\temp\Todo projeto
) else if exist "%PASTA_INSTALACAO%\temp\Todo Projeto" (
    echo Encontrada pasta: Todo Projeto
    set PASTA_ORIGEM=%PASTA_INSTALACAO%\temp\Todo Projeto
) else (
    echo Usando pasta temp diretamente
    set PASTA_ORIGEM=%PASTA_INSTALACAO%\temp
)

:: Copiar arquivos
echo Copiando arquivos para %PASTA_INSTALACAO%...
xcopy /E /I /Y "%PASTA_ORIGEM%\*" "%PASTA_INSTALACAO%\" >nul

:: Limpar temp
rmdir /S /Q "%PASTA_INSTALACAO%\temp"

echo [OK] Projeto baixado
echo.

:: DETERMINAR ONDE ESTÁ O CONFIG.PY
if exist "%PASTA_INSTALACAO%\config.py" (
    set PASTA_CONFIG=%PASTA_INSTALACAO%
    echo Config encontrado na raiz
) else if exist "%PASTA_INSTALACAO%\Todo projeto\config.py" (
    set PASTA_CONFIG=%PASTA_INSTALACAO%\Todo projeto
    echo Config encontrado em Todo projeto
) else if exist "%PASTA_INSTALACAO%\Todo Projeto\config.py" (
    set PASTA_CONFIG=%PASTA_INSTALACAO%\Todo Projeto
    echo Config encontrado em Todo Projeto
) else if exist "%PASTA_INSTALACAO%\Servidor-Python-main\config.py" (
    set PASTA_CONFIG=%PASTA_INSTALACAO%\Servidor-Python-main
    echo Config encontrado em Servidor-Python-main
) else (
    :: Se não encontrar, assume a raiz
    set PASTA_CONFIG=%PASTA_INSTALACAO%
    echo Usando raiz como pasta de configuracao
)

set CONFIG_PATH=%PASTA_CONFIG%\config.py
echo Config path: %CONFIG_PATH%
echo.

:: Perguntar pasta do repositório
echo.
echo [2/6] Configuracao da pasta de repositorio
echo Digite o caminho da pasta que voce deseja usar como repositorio de arquivos
echo (ex: C:\MeusArquivos, D:\Documentos, etc)
echo Ou pressione ENTER para usar a pasta padrao: %USERPROFILE%\MeuDriveRepositorio
echo.

set /p PASTA_REPOSITORIO=
if "%PASTA_REPOSITORIO%"=="" set PASTA_REPOSITORIO=%USERPROFILE%\MeuDriveRepositorio

:: Criar pasta do repositório se não existir
if not exist "%PASTA_REPOSITORIO%" mkdir "%PASTA_REPOSITORIO%"

echo [OK] Pasta do repositorio: %PASTA_REPOSITORIO%
echo.

:: Configurar o config.py
echo [3/6] Configurando arquivos...

:: Substituir a linha da PASTA_BASE no config.py
powershell -Command "$caminho = '%PASTA_REPOSITORIO%' -replace '\\', '\\'; $conteudo = Get-Content '%CONFIG_PATH%'; $novoConteudo = $conteudo -replace 'PASTA_BASE = os\.path\.abspath\(.*?\)', \"PASTA_BASE = os.path.abspath(r'$caminho')\"; $novoConteudo | Set-Content '%CONFIG_PATH%' -Encoding UTF8"

echo [OK] Configuracao concluida
echo.

:: Criar ambiente virtual
echo [4/6] Criando ambiente virtual...
cd /d "%PASTA_CONFIG%"

:: Remover venv antigo se existir
if exist "%PASTA_CONFIG%\venv" (
    echo Removendo ambiente virtual antigo...
    rmdir /S /Q "%PASTA_CONFIG%\venv"
)

:: Criar novo ambiente virtual
python -m venv venv

:: VERIFICAR SE O VENV FOI CRIADO CORRETAMENTE
if not exist "%PASTA_CONFIG%\venv\Scripts\activate" (
    echo [ERRO] Falha ao criar ambiente virtual!
    echo Tentando metodo alternativo...
    python -m venv --without-pip venv
    python -m ensurepip --upgrade
    "%PASTA_CONFIG%\venv\Scripts\python" -m pip install --upgrade pip
)

echo [OK] Ambiente virtual criado em %PASTA_CONFIG%\venv
echo.

:: Instalar dependências
echo [5/6] Instalando dependencias...

:: Atualizar pip
call "%PASTA_CONFIG%\venv\Scripts\python" -m pip install --upgrade pip

:: Verificar se requirements.txt existe
if exist "%PASTA_CONFIG%\requirements.txt" (
    echo Instalando dependencias do requirements.txt...
    call "%PASTA_CONFIG%\venv\Scripts\pip" install -r requirements.txt
) else (
    echo requirements.txt nao encontrado. Instalando Flask diretamente...
    call "%PASTA_CONFIG%\venv\Scripts\pip" install flask
)

:: VERIFICAR SE O FLASK FOI INSTALADO
call "%PASTA_CONFIG%\venv\Scripts\python" -c "import flask" 2>nul
if errorlevel 1 (
    echo [AVISO] Flask nao instalado. Tentando novamente...
    call "%PASTA_CONFIG%\venv\Scripts\pip" install flask
) else (
    echo [OK] Flask instalado com sucesso
)

echo [OK] Dependencias instaladas
echo.

:: PROCURAR O SCRIPT DE INICIALIZAÇÃO
echo [6/6] Configurando atalhos...

set SCRIPT_INICIAR=
if exist "%PASTA_CONFIG%\iniciar.bat" (
    set SCRIPT_INICIAR=%PASTA_CONFIG%\iniciar.bat
    echo Script de inicializacao encontrado na raiz
) else if exist "%PASTA_CONFIG%\Todo projeto\iniciar.bat" (
    set SCRIPT_INICIAR=%PASTA_CONFIG%\Todo projeto\iniciar.bat
    echo Script encontrado em Todo projeto
) else if exist "%PASTA_CONFIG%\Todo Projeto\iniciar.bat" (
    set SCRIPT_INICIAR=%PASTA_CONFIG%\Todo Projeto\iniciar.bat
    echo Script encontrado em Todo Projeto
) else if exist "%PASTA_CONFIG%\Servidor-Python-main\iniciar.bat" (
    set SCRIPT_INICIAR=%PASTA_CONFIG%\Servidor-Python-main\iniciar.bat
    echo Script encontrado em Servidor-Python-main
)

:: Perguntar sobre atalhos
echo.
echo Deseja criar atalhos na area de trabalho? (S/N)
echo - Atalho para INICIAR o servidor
echo - Atalho para ABRIR a pagina web
set /p CRIAR_ATALHO=

:: CRIAR ATALHOS NA ÁREA DE TRABALHO
if /i "%CRIAR_ATALHO%"=="S" (
    set DESKTOP=%USERPROFILE%\Desktop
    
    if exist "%DESKTOP%" (
        echo Criando atalhos na area de trabalho...
        
        :: ATALHO 1: Para iniciar o servidor (se o script existir)
        if defined SCRIPT_INICIAR (
            if exist "%SCRIPT_INICIAR%" (
                copy "%SCRIPT_INICIAR%" "%DESKTOP%\MeuDrivePessoal-Iniciar.bat" >nul
                echo [OK] Atalho 1 criado: %DESKTOP%\MeuDrivePessoal-Iniciar.bat
            ) else (
                echo [AVISO] Script de inicializacao nao encontrado em %SCRIPT_INICIAR%
            )
        ) else (
            echo [AVISO] Script de inicializacao nao encontrado no projeto
        )
        
        :: ATALHO 2: Para abrir a pagina web
        echo [InternetShortcut] > "%DESKTOP%\MeuDrivePessoal-Abrir.url"
        echo URL=http://localhost:5000 >> "%DESKTOP%\MeuDrivePessoal-Abrir.url"
        echo IconIndex=0 >> "%DESKTOP%\MeuDrivePessoal-Abrir.url"
        echo [OK] Atalho 2 criado: %DESKTOP%\MeuDrivePessoal-Abrir.url
    ) else (
        echo [AVISO] Pasta Desktop nao encontrada em %DESKTOP%
    )
) else (
    echo Atalhos nao criados por opcao do usuario.
)

:: Criar atalho na pasta de instalação para abrir o site (sempre cria)
echo [InternetShortcut] > "%PASTA_CONFIG%\MeuDrivePessoal.url"
echo URL=http://localhost:5000 >> "%PASTA_CONFIG%\MeuDrivePessoal.url"
echo IconIndex=0 >> "%PASTA_CONFIG%\MeuDrivePessoal.url"
echo [OK] Atalho local criado em: %PASTA_CONFIG%\MeuDrivePessoal.url

echo [OK] Configuracao de atalhos concluida
echo.

:: OBTER O IP DA MÁQUINA PARA MOSTRAR NO RELATÓRIO
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%a
set IP=%IP: =%

:: Mostrar relatório final
echo.
echo ===================================================
echo    ✅ INSTALACAO CONCLUIDA COM SUCESSO!
echo ===================================================
echo.
echo 📁 Projeto instalado em: %PASTA_CONFIG%
echo 📁 Repositorio de arquivos: %PASTA_REPOSITORIO%
echo.
echo 🚀 Para iniciar o servidor:
if defined SCRIPT_INICIAR (
    echo    • Script: %SCRIPT_INICIAR%
) else (
    echo    • Navegue ate a pasta e execute: iniciar.bat
)

if /i "%CRIAR_ATALHO%"=="S" (
    echo    • Atalho na area de trabalho: MeuDrivePessoal-Iniciar.bat
)
echo.
echo 🌐 Para acessar o servidor:
echo    • Local: http://localhost:5000
echo    • Rede:  http://%IP%:5000
if /i "%CRIAR_ATALHO%"=="S" (
    echo    • Atalho na area de trabalho: MeuDrivePessoal-Abrir.url
)
echo.
echo ===================================================

:: Perguntar sobre iniciar agora
echo.
echo Deseja iniciar o servidor agora? (S/N)
set /p INICIAR_AGORA=

:: Iniciar servidor se o usuário quiser
if /i "%INICIAR_AGORA%"=="S" (
    echo.
    echo Iniciando servidor...
    
    if defined SCRIPT_INICIAR (
        if exist "%SCRIPT_INICIAR%" (
            echo Executando: %SCRIPT_INICIAR%
            start "Meu Drive Pessoal" cmd /k "%SCRIPT_INICIAR%"
            
            :: Aguardar 3 segundos para o servidor iniciar
            timeout /t 3 /nobreak >nul
            
            :: Abrir navegador
            start http://localhost:5000
            
            echo Servidor iniciado em nova janela
        ) else (
            echo [ERRO] Script de inicializacao nao encontrado: %SCRIPT_INICIAR%
        )
    ) else (
        echo [ERRO] Script de inicializacao nao definido
    )
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul