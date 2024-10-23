#1 Creación de la Base de Datos:----------------------------------
CREATE DATABASE gestion_usuarios;
#2 Selecciona la base de datos para empezar a trabajar en ella:---
USE gestion_usuarios;
#3 Creación de las Tablas Usuario y Acceso------------------------


CREATE TABLE Usuario (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    usuario_Nombre VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL, -- Almacenar el hash de la contraseña
    E_mail VARCHAR(100) UNIQUE NOT NULL,
    creado_En DATETIME DEFAULT CURRENT_TIMESTAMP,
    Estado ENUM('active', 'inactive', 'deleted') DEFAULT 'active',
    Roles VARCHAR(50)
);
#4 Información Adicional en la Tabla Usuario:-------------------------------------------------------------------------------
# Fecha de Creación: La columna created_at es útil para realizar análisis históricos y rastrear la antigüedad de las cuentas.
#Estado del Usuario: Agregar una columna Estado (por ejemplo, 'active', 'inactive', 'deleted') permite gestionar el ciclo de 
#vida de los usuarios de manera más flexible.
#Roles: Si tu aplicación requiere diferentes niveles de acceso, puedes agregar una columna Roles para definir los permisos de 
#cada usuario.

CREATE TABLE Acceso (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Fecha_Ingreso DATETIME NOT NULL,
    Fecha_Salida DATETIME,
    Usuario_Logueado INT,
    dirección_IP VARCHAR(50),
    dispositivo_Info VARCHAR(100),
    FOREIGN KEY (Usuario_Logueado) REFERENCES Usuario(id) ON DELETE RESTRICT
);
#5 Optimización de la Tabla Acceso:-----------------------------------------------------------------------------------------
#Índices: Además de Usuario_Logueado, considera agregar índices a las columnas Fecha_Ingreso y Fecha_Salida si realizas muchas 
#consultas de rango en estas fechas.
#Información Adicional: Puedes agregar columnas como dirección_IP o dispositivo_Info para rastrear desde dónde se realizan los accesos.

CREATE INDEX idx_fecha_ingreso ON Acceso (Fecha_Ingreso);
CREATE INDEX idx_fecha_salida ON Acceso (Fecha_Salida);
CREATE INDEX idx_Usuario_Logueado on Acceso (Usuario_Logueado);
SHOW INDEX FROM Acceso;
SELECT * FROM Acceso
WHERE Fecha_Ingreso BETWEEN '2024-08-01' AND '2024-08-31';
#6 Índices:------------------------------------------------------------------------------------------------------------------ 
#Además de Usuario_Logueado, considera agregar índices a las columnas Fecha_Ingreso y Fecha_Salida si realizas muchas consultas 
#de rango en estas fechas.

INSERT INTO Usuario (usuario_Nombre, Password, E_mail, Roles, creado_En) VALUES
('RINCONAvril', 'hash_fuerte', 'aerincnvergara@escuelasproa.edu.ar', 'User','2024-09-22 10:30:00'),
('GALANCandelaria', 'hash_seguro', 'cgalanvergara@escuelasproa.edu.ar', 'Admin','2024-08-21 09:30:00'),
('LURASCHITiara', 'hash_fuerte', 'tluraschi@escuelasproa.edu.ar','User','2024-07-24 08:30:00' ),
('MERCADOMatias', 'hash_seguro', 'mbmercado@escuelasproa.edu.ar','Admin','2024-06-23 11:30:00' ),
('ARREGUIAgustina', 'hash_seguro', 'aarreguipicca@escuelasproa.edu.ar', 'User','default');

INSERT INTO Acceso (Fecha_Ingreso, Fecha_Salida, Usuario_Logueado, dirección_IP, dispositivo_Info) VALUES
('2024-08-06 17:00:00', '2024-08-06 19:00:00', 1, '192.168.1.100', 'Windows 10'),
('2024-08-05 14:00:00', '2024-08-05 16:00:00', 1, '182.127.2.100', 'Windows 11'),
('2024-09-04 10:30:00', '2024-09-04 12:30:00', 2, '184.120.1.100', 'Android 13'),
('2024-09-03 08:00:00', NULL, 3, '172.16.10.20', 'iPhone 14');

#7 Operaciones CRUD para la Tabla Usuario: Agregar un Nuevo Usuario:----------------------------------------------------------
INSERT INTO Usuario (usuario_Nombre, Password, E_mail, Roles, creado_En) VALUES
('ZARATEJazmín', 'hash_fuerte', 'jzarate@escuelasproa.edu.ar', 'Adm', '2024-10-20 20:30:00');

# Modificar un Usuario:----------------------------------------------------------
UPDATE Usuario
SET E_mail = 'aarregui@escuelasproa.edu.ar'
WHERE User_name = 'ARREGUIAgustina';
# Eliminar un Usuario (por User_name o E_mail): ------------------------------------
DELETE FROM Usuario
WHERE User_name = 'ZARATEJazmín';
-------------------------------------------------------------------------------------
DELETE FROM Usuario
WHERE E_mail = 'jzarate@escuelasproa.edu.ar';
# Buscar por User_name o E_mail:------------------------------------------------------
SELECT * FROM Usuario
WHERE User_name = 'MERCADOMatias';
-------------------------------------------------------------------------------------
SELECT * FROM Usuario
WHERE E_mail = 'mbmercado@escuelasproa.edu.ar';
# Mostrar Todos los Usuarios:--------------------------------------------------------
SELECT * FROM Usuario;
#8 Consultas SQL con JOIN - Obtener Todos los Accesos de un Usuario Específico:------
SELECT Acceso.ID, Acceso.Fecha_Ingreso, Acceso.Fecha_Salida
FROM Acceso
JOIN Usuario ON Acceso.Usuario_Logueado = Usuario.ID
WHERE Usuario.usuario_Nombre = 'GALANCandelaria';
# Listar Usuarios con la Cantidad de Accesos que Tienen:-----------------------------
SELECT Usuario.usuario_Nombre, Usuario.E_mail, COUNT(Acceso.ID) AS cantidadAccesos
FROM Usuario
LEFT JOIN Acceso ON Usuario.ID = Acceso.Usuario_Logueado
GROUP BY Usuario.ID, Usuario.usuario_Nombre, Usuario.E_mail;





