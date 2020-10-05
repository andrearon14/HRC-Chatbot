/*----------------------------------------------------- 
creado por adrian
-----------------------------------------------------*/
DROP DATABASE IF EXISTS hrc;
CREATE DATABASE hrc;
USE hrc;

CREATE TABLE usuario(
id int auto_increment,
foto varchar(200),
nombre varchar(100),
administrador bool,
idempleado int,
primary	key (id)
);

CREATE TABLE empleado(
id int auto_increment,
empresa int,
documento varchar(100),
nombre varchar(100),
direccion varchar(100),
correo varchar(100),
activo varchar(100),
diasLicenciaDisponibles int,
notificaciones varchar(1000),
adelantoPermitido int,
foto varchar(100),
cargo varchar(100),
sexo char(1),
primary key (id)
);

CREATE TABLE area(
id int auto_increment,
nombre varchar(100),
primary key (id)
);

CREATE TABLE areaEmpleado(
idarea int,
idempleado int,
primary key (idarea, idempleado)
);

CREATE TABLE marcasEmpleados(
id int auto_increment,
idempleado int,
fecha date,
horaentrada time,
horasalida time,
horasextra int,
primary key (id)
);

CREATE TABLE licencia(
id int auto_increment,
idempleado int,
fechaComienzo datetime,
fechaFinal datetime,
confirmada bool,
razonRechazada varchar(200),
primary key (id)
);

CREATE TABLE empresa(
id int auto_increment,
rut varchar(100) not null,
nombre varchar(100) not null,
correo varchar(100),
telefono varchar(100),
direccion varchar(100),
primary key (id)
);

CREATE TABLE tipoSugerencia(
id varchar(100) not null,
text varchar(200),
primary key (id)
);

CREATE TABLE sugerencia(
id int auto_increment ,
idTipoSugerencia varchar(100) not null,
fecha datetime,
idempresa int,
idempleado int,
comentario text,
primary key (id)
);
