# 1. Usar una imagen oficial de Python
FROM python:3.11-slim

# 2. Crear y usar un directorio de trabajo
WORKDIR /gestion_239

# 3. Copiar los archivos de tu proyecto al contenedor
COPY . .

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Exponer el puerto que Streamlit usa (8501 por defecto)
EXPOSE 8501

# 6. Comando para iniciar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
