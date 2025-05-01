@echo off
echo ===============================
echo Deteniendo la app de Gastos Familiares...
echo ===============================

REM Detener contenedor
docker compose down

echo [INFO] App detenida correctamente.
pause
