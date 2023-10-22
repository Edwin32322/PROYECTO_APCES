CREATE DATABASE BD_APCES;

USE BD_APCES;

DROP database BD_APCES;

CREATE TABLE Acta(
	id_Acta int(10) primary key auto_increment,
    fecha_Acta date not null,
    hora_Inicio_Acta datetime not null,
    hora_Fin_Acta datetime not null,
    id_Citacion_FK int(10) not null
);

CREATE TABLE Citacion(
	id_Citacion int(10) primary key auto_increment,
    fecha_Citacion date not null,
    hora_Citacion datetime not null,
    descripcion_Citacion varchar(30),
    asunto_Citacion varchar(30),
    id_Llamado_Atencion_1_FK int(10) not null,
    id_Llamado_Atencion_2_FK int(10)
);

CREATE TABLE LlamadoAtencion(
	id_Llamado_Atencion int(10) primary key auto_increment,
    fecha_Llamado_Atencion date not null,
    motivo_Llamado_Atencion varchar(150) not null,
    id_Falta_FK int(10) not null,
    id_Usuario_FK int(10) not null,
    id_Aprendiz_FK int(10) not null
);
CREATE TABLE CasoAprendiz(
	id_Aprendiz int(10) primary key auto_increment,
    tipoDoc_Aprendiz varchar(30) not null,
    num_Documento_Aprendiz int(10) not null,
    correo_Aprendiz varchar(30) not null,
    nombre_Aprendiz varchar(30) not null,
    estado_Matricula varchar(30) not null,
    direccion_Aprendiz varchar(30) not null,
    num_Ficha_FK int(10) not null
);

CREATE TABLE FichaFormacion(
	num_Ficha int(10) primary key auto_increment,
    nombre_Programa_Formacion varchar(50) not null
);

CREATE TABLE Falta(
	id_Falta int(10) primary key auto_increment,
    tipo_Falta varchar(30) not null,
    descripcion_Falta varchar(100) not null
);

CREATE TABLE Usuario(
	id_Usuario int(10) primary key auto_increment ,
    numero_Documento_Usuario int(10) not null,
    tipoDoc_Usuario varchar(30) not null,
    telefono_Usuario varchar(15) not null,
    correo_Usuario varchar(30) not null,
    nombre_Usuario varchar(30) not null,
    contrasena_Usuario varchar(255) not null,
    imagen_Usuario LongBlob null,
    estado_Usuario boolean not null,
    id_Rol_FK int(10) not null
);

CREATE TABLE Rol(
	id_Rol int(10) primary key auto_increment,
    descripcion_Rol varchar(50) not null
);


ALTER TABLE Acta ADD CONSTRAINT FK_Acta_Citacion FOREIGN KEY (id_Citacion_FK) REFERENCES Citacion(id_Citacion);
ALTER TABLE Citacion ADD CONSTRAINT FK_Citacion_Llamado_Atencion_1 FOREIGN KEY (id_Llamado_Atencion_1_FK) REFERENCES LlamadoAtencion(id_Llamado_Atencion);
ALTER TABLE Citacion ADD CONSTRAINT FK_Citacion_Llamado_Atencion_2 FOREIGN KEY (id_Llamado_Atencion_2_FK) REFERENCES LlamadoAtencion(id_Llamado_Atencion);
ALTER TABLE LlamadoAtencion ADD CONSTRAINT FK_Llamado_Atencion_Falta FOREIGN KEY (id_Falta_FK) REFERENCES Falta(id_Falta);
ALTER TABLE LlamadoAtencion ADD CONSTRAINT FK_Llamado_Atencion_Usuario FOREIGN KEY (id_Usuario_FK) REFERENCES Usuario(id_Usuario);
ALTER TABLE LlamadoAtencion ADD CONSTRAINT FK_Llamado_Atencion_Aprendiz FOREIGN KEY (id_Aprendiz_FK) REFERENCES CasoAprendiz(id_Aprendiz);
ALTER TABLE CasoAprendiz ADD CONSTRAINT FK_Caso_Aprendiz_Ficha FOREIGN KEY (num_Ficha_FK) REFERENCES FichaFormacion(num_Ficha);
ALTER TABLE Usuario ADD CONSTRAINT FK_Usuario_Rol FOREIGN KEY (id_Rol_FK) REFERENCES Rol(id_Rol);


-- VISTA ENCARGADA DE MOSTRAR LOS APRENDICEZ A LOS CUALES SE LES DEBE HACER EL PROCESO DE CITACION --

CREATE VIEW view_Aprendices_Para_Citacion AS
SELECT cp.id_Aprendiz, cp.nombre_Aprendiz, f.tipo_Falta, COUNT(cp.id_Aprendiz) AS CantidadLlamados, l.id_Usuario_FK
FROM CasoAprendiz cp
INNER JOIN LlamadoAtencion l ON cp.id_Aprendiz = l.id_Aprendiz_FK
INNER JOIN Falta f ON l.id_Falta_FK = f.id_Falta
GROUP BY cp.id_Aprendiz, l.id_Usuario_FK, f.tipo_Falta
HAVING f.tipo_Falta = 'Falta Grave' OR COUNT(cp.id_Aprendiz) > 1;

SELECT * FROM view_Aprendices_Para_Citacion;