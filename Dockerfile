# Usa una imagen base de Python
FROM python:3.11.2

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expón el puerto en el que se ejecutará tu aplicación
EXPOSE 8000

# Comando para ejecutar la migración inicial y crear el usuario admin (puede variar según tu proyecto)
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('compumax@soporte.com', 'compumax@soporte.com', '@compumax2023')" | python manage.py shell

# Comando para arrancar Gunicorn y ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "flupi.wsgi"]