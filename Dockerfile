FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements e instalar dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Entrenar el modelo automáticamente
RUN rasa train

# Puerto para la API de Rasa
EXPOSE 5005

# Ejecutar el servidor de Rasa
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--model", "/app/models"]
