create database flupi_db;

use flupi_db;

create table points(
    id int primary key AUTO_INCREMENT,
    avengers int,
    quimbolitos int,
    usuario varchar(100) not null,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);