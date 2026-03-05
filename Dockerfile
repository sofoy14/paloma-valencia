# Dockerfile para Railway
FROM python:3.9-slim

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data reports

# Script de inicio
RUN echo '#!/bin/bash\nexec gunicorn app:app --bind 0.0.0.0:"${PORT:-5000}" --workers 1 --threads 2 --timeout 120' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
