create database flupi_db;

use flupi_db;

create table points(
    id int primary key AUTO_INCREMENT,
    avengers int,
    quimbolitos int,
    fecha date not null
);