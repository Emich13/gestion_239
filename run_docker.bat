@echo off
echo ===============================
echo Levantando la app con Docker Compose...
echo ===============================

REM Reconstruir imagen y levantar contenedor
docker compose up --build

REM Si cerrás esta ventana, la app se detiene
