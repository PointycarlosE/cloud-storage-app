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
echo [1/5] Baixando projeto do GitHub...
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
    set PASTA_CONFIG=%PASTA_INSTALACAO%
    echo Usando raiz como pasta de configuracao
)

echo.
echo ===================================================
echo    📂 CONFIGURACAO DA PASTA DE REPOSITORIO
echo ===================================================
echo.

:: Perguntar pasta do repositório
echo Digite o caminho da pasta que voce deseja usar como repositorio de arquivos
echo (ex: C:\Users\SeuUsuario\MeusArquivos)
echo.
set /p PASTA_REPOSITORIO=

if "%PASTA_REPOSITORIO%"=="" (
    echo [ERRO] Voce precisa digitar um caminho para o repositorio!
    pause
    exit /b 1
)

:: Criar pasta do repositório
if not exist "%PASTA_REPOSITORIO%" (
    mkdir "%PASTA_REPOSITORIO%"
    echo [OK] Pasta do repositorio criada: %PASTA_REPOSITORIO%
) else (
    echo [OK] Pasta do repositorio ja existe: %PASTA_REPOSITORIO%
)

echo.
echo [2/5] Configurando arquivos...

:: Configurar o config.py com a pasta base
powershell -Command "$caminho = '%PASTA_REPOSITORIO%' -replace '\\', '\\'; $conteudo = Get-Content '%PASTA_CONFIG%\config.py'; $novoConteudo = $conteudo -replace 'PASTA_BASE = os\.path\.abspath\(.*?\)', \"PASTA_BASE = os.path.abspath(r'$caminho')\"; $novoConteudo | Set-Content '%PASTA_CONFIG%\config.py' -Encoding UTF8"

echo [OK] Configuracao concluida
echo.

:: Criar ambiente virtual
echo [3/5] Criando ambiente virtual...
cd /d "%PASTA_CONFIG%"

if exist "%PASTA_CONFIG%\venv" (
    echo Removendo ambiente virtual antigo...
    rmdir /S /Q "%PASTA_CONFIG%\venv"
)

python -m venv venv

if not exist "%PASTA_CONFIG%\venv\Scripts\activate" (
    echo [ERRO] Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual criado
echo.

:: Instalar dependências
echo [4/5] Instalando dependencias...

call "%PASTA_CONFIG%\venv\Scripts\python" -m pip install --upgrade pip
call "%PASTA_CONFIG%\venv\Scripts\pip" install flask flask-login python-dotenv

echo [OK] Dependencias instaladas
echo.

:: Criar script de inicialização
echo [5/5] Criando script de inicializacao...

echo @echo off > "%PASTA_CONFIG%\iniciar.bat"
echo title Meu Drive Pessoal - Servidor >> "%PASTA_CONFIG%\iniciar.bat"
echo color 0A >> "%PASTA_CONFIG%\iniciar.bat"
echo. >> "%PASTA_CONFIG%\iniciar.bat"
echo echo =================================================== >> "%PASTA_CONFIG%\iniciar.bat"
echo echo    🚀 INICIANDO MEU DRIVE PESSOAL >> "%PASTA_CONFIG%\iniciar.bat"
echo echo =================================================== >> "%PASTA_CONFIG%\iniciar.bat"
echo echo. >> "%PASTA_CONFIG%\iniciar.bat"
echo cd /d "%PASTA_CONFIG%" >> "%PASTA_CONFIG%\iniciar.bat"
echo call venv\Scripts\activate >> "%PASTA_CONFIG%\iniciar.bat"
echo for /f "tokens=2 delims=:" %%%%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%%%a >> "%PASTA_CONFIG%\iniciar.bat"
echo set IP=%%IP: =%% >> "%PASTA_CONFIG%\iniciar.bat"
echo echo [OK] Servidor disponivel em: >> "%PASTA_CONFIG%\iniciar.bat"
echo echo    • Local: http://localhost:5000 >> "%PASTA_CONFIG%\iniciar.bat"
echo echo    • Rede:  http://%%IP%%:5000 >> "%PASTA_CONFIG%\iniciar.bat"
echo echo. >> "%PASTA_CONFIG%\iniciar.bat"
echo echo Pressione CTRL+C para parar o servidor >> "%PASTA_CONFIG%\iniciar.bat"
echo echo =================================================== >> "%PASTA_CONFIG%\iniciar.bat"
echo echo. >> "%PASTA_CONFIG%\iniciar.bat"
echo python app.py >> "%PASTA_CONFIG%\iniciar.bat"
echo pause >> "%PASTA_CONFIG%\iniciar.bat"

echo [OK] Script de inicializacao criado
echo.

:: Criar atalhos
echo.
echo Deseja criar atalhos na area de trabalho? (S/N)
echo - Atalho para INICIAR o servidor
echo - Atalho para ABRIR a pagina web
set /p CRIAR_ATALHO=

if /i "%CRIAR_ATALHO%"=="S" (
    set DESKTOP=%USERPROFILE%\Desktop
    if exist "%DESKTOP%" (
        copy "%PASTA_CONFIG%\iniciar.bat" "%DESKTOP%\MeuDrivePessoal - Iniciar.bat" >nul
        echo [OK] Atalho 1 criado: %DESKTOP%\MeuDrivePessoal - Iniciar.bat
        
        echo [InternetShortcut] > "%DESKTOP%\MeuDrivePessoal - Abrir.url"
        echo URL=http://localhost:5000 >> "%DESKTOP%\MeuDrivePessoal - Abrir.url"
        echo IconIndex=0 >> "%DESKTOP%\MeuDrivePessoal - Abrir.url"
        echo [OK] Atalho 2 criado: %DESKTOP%\MeuDrivePessoal - Abrir.url
    ) else (
        echo [AVISO] Pasta Desktop nao encontrada
    )
)

:: OBTER O IP DA MÁQUINA
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
echo    • Execute: %PASTA_CONFIG%\iniciar.bat
if /i "%CRIAR_ATALHO%"=="S" (
    echo    • Atalho na area de trabalho: MeuDrivePessoal - Iniciar.bat
)
echo.
echo 🌐 Para acessar o servidor:
echo    • Local: http://localhost:5000
echo    • Rede:  http://%IP%:5000
if /i "%CRIAR_ATALHO%"=="S" (
    echo    • Atalho na area de trabalho: MeuDrivePessoal - Abrir.url
)
echo.
echo 🔐 PRIMEIRA EXECUCAO:
echo    Ao acessar pela primeira vez, voce sera redirecionado para a tela de criacao de conta.
echo    Defina seu usuario e senha para acessar o sistema.
echo.
echo ===================================================
echo.
echo Deseja iniciar o servidor agora? (S/N)
set /p INICIAR_AGORA=

if /i "%INICIAR_AGORA%"=="S" (
    echo.
    echo Iniciando servidor...
    start "Meu Drive Pessoal" cmd /k "%PASTA_CONFIG%\iniciar.bat"
    timeout /t 3 /nobreak >nul
    start http://localhost:5000
    echo Servidor iniciado!
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul