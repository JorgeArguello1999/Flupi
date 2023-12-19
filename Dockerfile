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

RUN echo 'Running collecstatic...'
RUN python manage.py collectstatic --no-input --settings=flupi.settings.production

RUN echo 'Applying migrations...'
RUN python manage.py migrate --settings=flupi.settings.production

RUN echo "Creando superusuario"
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('compumax@soporte.com', 'compumax@soporte.com', '@compumax2023')" | python manage.py shell --settings=flupi.settings.production


RUN echo 'Running server...'
# CMD ["gunicorn --env DJANGO_SETTINGS_MODULE=flupi.settings.production flupi.wsgi --bind 0.0.0.0:8000"]
CMD ["gunicorn", "--env", "DJANGO_SETTINGS_MODULE=flupi.settings.production", "flupi.wsgi", "--bind", "0.0.0.0:8000"]