@echo off
title Meu Drive Pessoal - Servidor
color 0A

echo ===================================================
echo    🚀 INICIANDO MEU DRIVE PESSOAL
echo ===================================================
echo.

:: Ir para a pasta do projeto
cd /d "%~dp0"

:: Verificar se venv existe
if not exist "venv\Scripts\activate" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute o instalador novamente.
    pause
    exit /b 1
)

:: Ativar ambiente virtual
echo [OK] Ativando ambiente virtual...
call venv\Scripts\activate

:: Verificar se Flask esta instalado
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [AVISO] Flask nao encontrado. Instalando...
    pip install flask
)

:: Mostrar IP da maquina
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%a
set IP=%IP: =%

echo.
echo [OK] Servidor disponivel em:
echo    • Local: http://localhost:5000
echo    • Rede:  http://%IP%:5000
echo.
echo Pressione CTRL+C para parar o servidor
echo ===================================================
echo.

:: Iniciar servidor
python app.py

pause