FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar Rasa
RUN pip install --no-cache-dir \
    rasa==3.6.2 \
    transformers \
    huggingface_hub

# Copiar proyecto
COPY . .

# Puerto para Rasa API
EXPOSE 5005

# Comando sin el argumento --host que causa problemas
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--model", "/app/models"]