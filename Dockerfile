FROM python:3.11

WORKDIR /app

# Copia todos los archivos excepto el directorio APPS/
COPY ./ /app/
COPY ./APPS/ /app/APPS/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "main:app"]