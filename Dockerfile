# 1. Usar una imagen oficial liviana de Python
FROM python:3.11-slim

# 2. Instalar dependencias del sistema necesarias para algunas bibliotecas (como pandas y psycopg2-binary)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Crear y usar un directorio de trabajo
WORKDIR /gestion_239

# 4. Copiar los archivos de tu proyecto al contenedor
COPY . .

# 5. Instalar las dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Exponer el puerto que Streamlit usa (8501 por defecto)
EXPOSE 8501

# 7. Comando para iniciar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
