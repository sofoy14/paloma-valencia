# Dockerfile para deploy en Railway/Render
FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Crear directorios necesarios
RUN mkdir -p data reports

# Puerto que usa la app (Railway lo sobreescribe)
EXPOSE 5000

# Comando para iniciar - usar shell para expandir variables
CMD exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120
