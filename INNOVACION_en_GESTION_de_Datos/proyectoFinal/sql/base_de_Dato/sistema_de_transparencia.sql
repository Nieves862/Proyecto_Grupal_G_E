#proyectoFinal ------------ Sistema de TRANSPARENCIA -----------------------------------------------------------------

create database sistema_de_transparencia;
--
use sistema_de_transparencia;
--
CREATE TABLE cuarto_año (
    ID_Estudiante int (3) zerofill auto_increment primary key, -- "zerofill" rellena con ceros los espacios disponibles a la izquierda
    Apellido VARCHAR(20) NOT NULL,
    Nombre VARCHAR(15) NOT NULL,
    E_mail VARCHAR(40) NULL,
    Sexo CHAR(1) NULL,
    DNI INT(8) NOT NULL,
    Fecha_De_Nacimiento DATE NOT NULL,
    Edad INT UNSIGNED NOT NULL,
    Dirección VARCHAR(35),
    Localidad VARCHAR(20),
    Provincia VARCHAR(15),
    ID_Padre INT, -- Clave foránea que referencia a la tabla Usuario
    FOREIGN KEY (ID_Padre) REFERENCES Usuario(ID_Usuario)
);

--
insert into cuarto_año (Apellido, Nombre, E_mail, Sexo, DNI, Fecha_De_Nacimiento, Edad, Dirección, Localidad, Provincia, ID_Padre) values 
('PEREYRA', 'Felipe', 'fgpereyrapriselac@escuelasproa.edu.ar','M', '48452841', '2008/04/30','16', 'Independencia', 'Despeñaderos', 'Cba', '841'),
('QUINTEROS', 'Candela', 'lcquinterosarce@escuelasproa.edu.ar','F', '49017754', '2008/09/15','16', 'Pedro Medrano', 'Despeñaderos', 'Cba', '754'),
('ACUÑA', 'Maximo', 'macunaoses@escuelasproa.edu.ar','M', '48455253', '2008/07/04','16', 'Rafaél Nuñez', 'Despeñaderos', 'Cba', '253'),
('MONCHIETTI', 'Benjamín', 'rbmonchiettiromero@escuelasproa.edu.ar', 'M', '49223054', '2008/12/19','15', 'Figeroa Alcorta', 'Despeñaderos', 'Cba', '492'),
('BENAVIDEZ', 'Ana', 'albenavidez@escuelasproa.edu.ar','F', '48452858', '2008/07/23','16', 'Pellegrini', 'Despeñaderos', 'Cba', '858');

--
ALTER TABLE cuarto_año
ADD COLUMN ID_Padre INT NULL,
ADD FOREIGN KEY (ID_Padre) REFERENCES Usuario(ID);

ALTER TABLE cuarto_año
MODIFY COLUMN ID_Estudiante INT AUTO_INCREMENT;

CREATE INDEX idx_cuarto_año_Apellido ON cuarto_año (Apellido);

--
CREATE TABLE Usuario (
    ID_Usuario INT PRIMARY KEY,
    Nombre_Padre VARCHAR(30) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL, -- Almacenar el hash de la contraseña
    E_mail VARCHAR(50) UNIQUE NOT NULL,
    creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    Estado ENUM('active', 'inactive', 'deleted') DEFAULT 'active',
    Roles VARCHAR(40) -- Para definir los roles del usuario (Ej: Padre)
);

 -- Información Adicional en la Tabla Usuario:---------------------------------------------------------------------------------
 -- Fecha de Creación: La columna creado_En es útil para realizar análisis históricos y rastrear la antigüedad de las cuentas.
 -- Estado: Agregar una columna Estado (por ejemplo, 'active', 'inactive', 'deleted') permite gestionar el ciclo de vida de los 
 -- usuarios de manera más flexible.
 -- Roles: Si la aplicación requiere diferentes niveles de acceso, puedes agregar una columna Roles para definir los permisos de 
 -- cada usuario.

--
INSERT INTO Usuario (ID_Usuario, Nombre_Padre, Password, E_mail, creado_En, Estado, Roles) VALUES
('858', 'BENAVIDEZ Alfredo', '858 hash_fuerte', 'valfredo@gmail.com.ar',NOW(), 'active', 'PADRE'),
('492','MONCHIETTI Diego', '492 hash_seguro', 'cdiego@gmail.com.ar', NOW(), 'active','PADRE'),
('253','ACUÑA Matías', '253 hash_fuerte', 'cmatías@gmail.com.ar', NOW(), 'active','PADRE' ),
('754','QUINTEROS Emmanuel', '754 hash_seguro', 'remmanuel@gmail.com.ar', NOW(), 'active','PADRE' ),
('841','PEREYRA Juan', '841 hash_seguro', 'pjuan@gmail.com.ar', NOW(), 'active','PADRE');

-- Selecciones ---------------------------------------------------------------------------------------------------------------------      
       select @@sql_safe_updates;
       set SQL_SAFE_UPDATES=1;
       set SQL_SAFE_UPDATES=0;
       --       
       update cuarto_año set Provincia ='Córdoba';
       --       
       describe cuarto_año;
       --
       SELECT * FROM cuarto_año ORDER BY apellido ASC, nombre ASC;
       --
       SELECT * FROM cuarto_año WHERE UPPER(DNI) = UPPER('48452858');
       --
     
CREATE TABLE IF NOT EXISTS materia(
ID_Materia INT NOT NULL AUTO_INCREMENT,
Espacio VARCHAR(25) NOT NULL,
Profesor VARCHAR(25) NOT NULL,
Detalle TEXT NULL DEFAULT NULL,
Carga_Horaria INT NOT NULL,
PRIMARY KEY (ID_Materia)
);

--
INSERT INTO materia (Espacio, Profesor, Detalle, Carga_Horaria) VALUES
('Estructura & Almacenamiento III', 'VILLALBA Valeria N', 'MySQL WORKBENCH', 3),
('Club de Ciencias', 'VILLALBA Valeria N', 'Robótica', 2);

CREATE INDEX idx_materia_Profesor ON materia (Profesor);

--
CREATE TABLE Asistencia (
    ID_Asistencia INT AUTO_INCREMENT PRIMARY KEY,
    ID_Estudiante INT NOT NULL,  -- Clave foránea que referencia al estudiante
    Fecha DATE NOT NULL,
    Estado ENUM('Presente', 'Ausente', 'Justificado', 'Injustificada') DEFAULT 'Ausente',
    Observaciones TEXT NULL,
    FOREIGN KEY (ID_Estudiante) REFERENCES cuarto_año(ID_Estudiante)
);

CREATE INDEX idx_asistencia_Fecha ON asistencia (Fecha);

-- Inserción de un registro donde el estudiante estuvo presente
INSERT INTO Asistencia (ID_Estudiante, Fecha, Estado, Observaciones)
VALUES (1, NOW(), 'Presente', 'Estudiante llegó a tiempo.');

-- Inserción de un registro donde el estudiante estuvo ausente
INSERT INTO Asistencia (ID_Estudiante, Fecha, Estado, Observaciones)
VALUES (2, NOW(), 'Ausente', 'Estudiante no se presentó.');

-- Inserción de un registro donde la ausencia fue justificada
INSERT INTO Asistencia (ID_Estudiante, Fecha, Estado, Observaciones)
VALUES (3, NOW(), 'Justificado', 'Ausencia justificada por enfermedad.');

-- Inserción de un registro sin observaciones
INSERT INTO Asistencia (ID_Estudiante, Fecha, Estado)
VALUES (4, NOW(), 'Presente');

--
CREATE TABLE grupo (
    ID_Grupo INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Grupo VARCHAR(50) NOT NULL
);

INSERT INTO grupo (Nombre_Grupo) VALUES
('Grupo de Estructura & Almacenamiento III'),
('Grupo de Robótica'),
('Grupo de Programación');

--
CREATE TABLE nota_formativa (
    ID_Nota INT AUTO_INCREMENT PRIMARY KEY,
    ID_Estudiante INT NOT NULL,
    ID_Materia INT NOT NULL,
    Fecha_Evaluación DATE NOT NULL,
    Nota DECIMAL(5,2) NOT NULL,
    Observación TEXT NULL,
    FOREIGN KEY (ID_Estudiante) REFERENCES cuarto_año(ID_Estudiante),
    FOREIGN KEY (ID_Materia) REFERENCES materia(ID_Materia)
);

INSERT INTO nota_formativa (ID_Estudiante, ID_Materia, Fecha_Evaluación, Nota, Observación) VALUES 
(1, 1, '2024-10-29', 8, 'Buen trabajo, muy ordenado y concreto'),
(2, 1, '2024-10-29', 7, 'Flojo pero tu puedes'),
(3, 1, '2024-10-29', 5, 'Este contenido te quedó PENDIENTE'),
(4, 1, '2024-10-29', 10, 'Excelente, Felicitaciones!');

CREATE INDEX idx_nota_formativa_estudiante_materia
ON nota_formativa (ID_Estudiante, ID_Materia);
--
CREATE TABLE Acceso (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Fecha_Ingreso DATETIME NOT NULL,
    Fecha_Salida DATETIME,
    Usuario_Logueado INT,
    dirección_IP VARCHAR(50),
    dispositivo_Info VARCHAR(100),
    Tabla_Accedida VARCHAR(50), -- Nueva columna para indicar la tabla accedida
    Acción_Realizada VARCHAR(50), -- Nueva columna para indicar la acción realizada
    FOREIGN KEY (Usuario_Logueado) REFERENCES Usuario(ID_Usuario)
);

 --
 -- Optimización de la Tabla Acceso:---------------------------------------------------------------------------------------------
 -- Índices: Además de Usuario_Logueado, se agregó índices a las columnas Fecha_Ingreso y Fecha_Salida por si realizan muchas 
 -- consultas de rango en estas fechas.
 -- Información Adicional: Se agregó columnas como dirección_IP o dispositivo_Info para rastrear desde dónde se realizan los accesos.
CREATE INDEX idx_fecha_ingreso ON Acceso (Fecha_Ingreso);
CREATE INDEX idx_fecha_salida ON Acceso (Fecha_Salida);
CREATE INDEX idx_Usuario_Logueado on Acceso (Usuario_Logueado);

 --
INSERT INTO Acceso (Fecha_Ingreso, Fecha_Salida, Usuario_Logueado, dirección_IP, dispositivo_Info, Tabla_Accedida, Acción_Realizada) VALUES 
(NOW(), NOW() + INTERVAL 1 HOUR, 858, '192.168.1.100', 'Windows 10', 'Usuario', 'Consultar'),
(NOW(), NOW() + INTERVAL 1 HOUR, 492, '10.0.0.5', 'Android', 'cuarto_año', 'Descargar'),
(NOW(), NOW() + INTERVAL 1 HOUR, 253, '10.0.0.5', 'Android', 'Usuario', 'Consultar'),
(NOW(), NOW() + INTERVAL 1 HOUR, 754, '192.168.1.100', 'Windows 10', 'cuarto_año', 'Descargar'),
(NOW(), NOW() + INTERVAL 1 HOUR, 841, '190.178.1.100', 'Windows 10', 'Usuario', 'Descargar');

--
CREATE TABLE Auditoria (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Tabla_Afectada VARCHAR(50),
    Registro_Anterior TEXT,
    Registro_Nuevo TEXT,
    ID_Usuario INT,
    Fecha_Hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);

 --
INSERT INTO Auditoria (Tabla_Afectada, Registro_Anterior, Registro_Nuevo, ID_Usuario, Fecha_Hora) VALUES 
('cuarto_año', '{"Nombre":"Felipe", "Edad":16}', '{"Nombre":"Felipe", "Edad":18}', 841, NOW());

 -- Operaciones CRUD para la Tabla Usuario: Agregar un Nuevo Usuario:----------------------------------------------------------
INSERT INTO Usuario (ID_Usuario, Nombre_Padre, Password, E_mail, creado_En, Estado, Roles) VALUES
('484', 'CASTAGNOVIZ Eduardo', '484 hash_fuerte', 'ceduardo@gmail.com.ar',NOW(), 'active', 'PADRE');

 -- Modificar un Usuario:-------------------------------------------------------------------------------------------------------
UPDATE Usuario
SET E_mail = 'balfredo@gmail.com.ar'
WHERE Nombre_Padre = 'BENAVIDEZ Alfredo';

 -- Eliminar un Usuario (por E_mail): -----------------------------------------------
DELETE FROM Usuario
WHERE E_mail = 'cdiego@gmail.com.ar';

 -- Buscar por E_mail:---------------------------------------------------------------
SELECT * FROM Usuario
WHERE E_mail = 'remmanuel@gmail.com.ar';

 -- Mostrar Todos los Usuarios:------------------------------------------------------
SELECT * FROM Usuario;

 -- Consultas SQL con JOIN ----------------------------------------------------------
SELECT Acceso.ID, Acceso.Fecha_Ingreso, Acceso.Fecha_Salida
FROM Acceso
JOIN Usuario ON Acceso.Usuario_Logueado = Usuario.ID_Usuario
WHERE Usuario.Nombre_Padre = 'QUINTEROS Candela';

SELECT cuarto_año.Nombre, Usuario.Nombre_Padre AS Nombre_Padre
FROM cuarto_año
INNER JOIN Usuario ON cuarto_año.ID_Padre = Usuario.ID_Usuario;

SELECT * FROM cuarto_año
INNER JOIN Usuario ON cuarto_año.ID_Padre = Usuario.ID_Usuario
WHERE Usuario.E_mail LIKE '%@gmail.com.ar';

SELECT c.Nombre, c.Apellido, c.Fecha_De_Nacimiento, u.Nombre_Padre, u.E_mail
FROM cuarto_año c
INNER JOIN Usuario u ON c.ID_Padre = u.ID_Usuario
WHERE c.ID_Estudiante = 003;

-- Para ver todos los índices de una tabla específica
SHOW INDEX FROM nota_formativa;
SHOW INDEX FROM asistencia; 
SHOW INDEX FROM auditoria;
SHOW INDEX FROM cuarto_año;
SHOW INDEX FROM grupo;
SHOW INDEX FROM materia;
SHOW INDEX FROM usuario;

-- Para ver todos los índices de la base de datos (requiere recorrer todas las tablas)
SHOW TABLES;  -- Obtiene una lista de todas las tablas


