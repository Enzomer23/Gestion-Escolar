-- Base de datos para el Sistema de Gestión Escolar GESJ
-- Provincia de San Juan, República Argentina

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS gestion_escolar;
USE gestion_escolar;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('Padre','Docente','Preceptor','Administrativo') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insertar usuarios de ejemplo
INSERT IGNORE INTO usuarios (nombre_usuario, contrasena, tipo_usuario) VALUES
('padre1', '1234', 'Padre'),
('docente1', 'abcd', 'Docente'),
('preceptor1', '5678', 'Preceptor'),
('admin1', 'adminpass', 'Administrativo');