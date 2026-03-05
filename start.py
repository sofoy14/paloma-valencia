#!/usr/bin/env python3
"""
Script de inicio para Railway - maneja el PORT correctamente
"""
import os
import sys

# Obtener PORT de las variables de entorno
port = os.environ.get('PORT', '5000')
print(f"[Start] Puerto configurado: {port}")

# Construir comando gunicorn
cmd = [
    'gunicorn',
    'app:app',
    '--bind', f'0.0.0.0:{port}',
    '--workers', '1',
    '--threads', '4',
    '--timeout', '120',
    '--access-logfile', '-',
    '--error-logfile', '-'
]

print(f"[Start] Ejecutando: {' '.join(cmd)}")

# Ejecutar gunicorn
os.execvp('gunicorn', cmd)
