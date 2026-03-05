# Dockerfile para deploy en la nube (Render, Railway, etc.)
FROM python:3.9-slim

# Instalar Chrome y dependencias
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno para Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Crear directorios necesarios
RUN mkdir -p data reports

# Puerto que usa la app
EXPOSE 5000

# Comando para iniciar
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "2", "--timeout", "120"]
