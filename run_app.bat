@echo off
SETLOCAL

echo ===============================
echo Lanzando la app de Gastos Familiares
echo ===============================

REM 1. Crear entorno si no existe
IF NOT EXIST .venv (
    echo [INFO] Creando entorno virtual...
    python -m venv .venv
)

REM 2. Activar entorno
echo [INFO] Activando entorno virtual...
call .venv\Scripts\activate.bat

REM 3. Instalar dependencias
echo [INFO] Instalando dependencias (si faltan)...
pip install --quiet -r requirements.txt

REM 4. Lanzar la app
echo [INFO] Ejecutando Streamlit...
streamlit run app.py

ENDLOCAL
