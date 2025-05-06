-- Database: sistema_login

CREATE DATABASE IF NOT EXISTS sistema_login
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sistema_login;

-- Tabla de usuarios (sin datos sensibles)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL COMMENT 'Almacenar solo hashes bcrypt',
    email VARCHAR(100) UNIQUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP NULL,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Usuario de aplicación (credenciales NO incluidas)
CREATE USER IF NOT EXISTS 'app_user'@'localhost' 
IDENTIFIED BY 'PASSWORD_NO_INCLUIR'; 

GRANT SELECT, INSERT, UPDATE ON sistema_login.* 
TO 'app_user'@'localhost';

FLUSH PRIVILEGES;
