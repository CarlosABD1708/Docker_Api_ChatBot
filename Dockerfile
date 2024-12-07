# Usa una imagen base de Python 3.12
FROM python:3.9-slim

# Instala SWI-Prolog y otras dependencias necesarias
RUN apt-get update && apt-get install -y \
    swi-prolog \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que correrá Flask
EXPOSE 5000

# Define el comando para ejecutar la API
CMD ["python", "prolog.py"]
