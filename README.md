# Flupi

![Flupi icon](Yo/logo.jpeg)

A software for manage a point in quality up class



> This is a example for my class

| ID   | Vengadores | Quimbolitos | Usuario   | Fecha               |
| ---- | ---------- | ----------- | --------- | ------------------- |
| 1    | 20         | 13          | Al3x_Argu | 2023-08-05 05:54:33 |



I use docker for database use this command for create docker image

```bash

docker run --name flupi_db -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql

```



## Database and Tables SQL code

```sql

create database flupi_db;

use flupi_db;

create table points(
    id int primary key AUTO_INCREMENT,
    avengers int,
    quimbolitos int,
    usuario varchar(100) not null,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

Tener en cuenta las siguientes depeendencias: `PyAudio`
para instalarlo en Linux (Ubuntu)

```bash
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg libav-tools
sudo pip install pyaudio
```



## This project isn't complete

A simple project, something idea please tell me.
