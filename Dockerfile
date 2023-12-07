# Usa la imagen base de Python 3.11
FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia todo el directorio de la aplicación al directorio de trabajo (/app)
COPY . /app

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación Flask con Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "main:app"]