# Define la imagen base: una versión ligera (slim) de Python 3.9 para ahorrar espacio
FROM python:3.9-slim

# Crea y establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias desde tu EC2 al contenedor
COPY requirements.txt .

# Instala las librerías de Python especificadas (Flask, mysql-connector, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicacion al directorio de trabajo del contenedor
COPY app_monolita.py .

# Define el comando que se ejecutará automáticamente al iniciar el contenedor
CMD ["python", "app_monolita.py"]
