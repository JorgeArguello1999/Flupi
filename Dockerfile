FROM python:3.11.2

WORKDIR /app

# Copia todos los archivos excepto el directorio APPS/
COPY . .

RUN apt-get update && apt-get install -y \
    portaudio19-dev

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]