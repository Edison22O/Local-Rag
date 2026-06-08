#!/bin/bash

echo "=== Iniciando Local RAG Lite ==="

# 1. Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "=> Creando entorno virtual..."
    python3 -m venv venv
fi

# 2. Activar entorno virtual e instalar dependencias
source venv/bin/activate
echo "=> Instalando dependencias necesarias..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Matar cualquier proceso previo en el puerto 5000
echo "=> Liberando puerto 5000..."
fuser -k 5000/tcp || true

# 4. Iniciar servidor
echo "=> Iniciando Servidor Lite..."
python -m uvicorn app:app --host 0.0.0.0 --port 5000
