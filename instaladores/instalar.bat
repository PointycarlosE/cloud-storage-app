@echo off
setlocal enabledelayedexpansion
title Instalador - Cloud Storage App

echo ==========================================
echo    INSTALADOR - CLOUD STORAGE APP
echo ==========================================
echo.

:: 1. Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! 
    echo Por favor, instale o Python 3.8+ e adicione ao PATH.
    echo Baixe em: https://www.python.org/
    pause
    exit /b 1
)

:: 2. Definir pasta de instalacao
set "DEFAULT_DIR=%CD%"
echo Pasta atual: %DEFAULT_DIR%
set /p "INSTALL_DIR=Deseja instalar nesta pasta? (S/N): "
if /i "%INSTALL_DIR%"=="N" (
    set /p "NEW_DIR=Digite o caminho completo da nova pasta: "
    if not exist "!NEW_DIR!" mkdir "!NEW_DIR!"
    cd /d "!NEW_DIR!"
)

:: 3. Criar Ambiente Virtual (VENV)
echo.
echo [1/4] Criando ambiente virtual (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar venv. Verifique permissoes.
    pause
    exit /b 1
)

:: 4. Instalar Dependencias
echo.
echo [2/4] Instalando dependencias (isso pode demorar)...
call venv\Scripts\activate
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias. Verifique sua internet.
    pause
    exit /b 1
)

:: 5. Configurar .env inicial
echo.
echo [3/4] Configurando variaveis de ambiente...
if not exist instance mkdir instance
if not exist instance\.env (
    echo FLASK_APP=run.py > instance\.env
    echo FLASK_ENV=development >> instance\.env
    echo SECRET_KEY=!RANDOM!!RANDOM!!RANDOM! >> instance\.env
    echo UPLOAD_FOLDER=uploads >> instance\.env
    echo MAX_CONTENT_LENGTH=524288000 >> instance\.env
    echo.
    echo [OK] Arquivo .env criado com chave secreta aleatoria.
)

:: 6. Criar Atalho na Area de Trabalho (via PowerShell)
echo.
echo [4/4] Criando atalho na Area de Trabalho...
set "SCRIPT_PATH=%CD%\run.py"
set "VENV_PYTHON=%CD%\venv\Scripts\python.exe"
set "SHORTCUT_NAME=Cloud Storage App.lnk"
set "DESKTOP_PATH=%USERPROFILE%\Desktop"

powershell -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%DESKTOP_PATH%\%SHORTCUT_NAME%'); $s.TargetPath='%VENV_PYTHON%'; $s.Arguments='%SCRIPT_PATH%'; $s.WorkingDirectory='%CD%'; $s.IconLocation='shell32.dll,44'; $s.Save()"

if %errorlevel% equ 0 (
    echo [OK] Atalho criado com sucesso na Area de Trabalho!
) else (
    echo [AVISO] Nao foi possivel criar o atalho automaticamente.
)

echo.
echo ==========================================
echo    INSTALACAO CONCLUIDA COM SUCESSO!
echo ==========================================
echo.
echo Para iniciar o servidor, use o atalho na Area de Trabalho
echo ou execute: venv\Scripts\python run.py
echo.
pause
