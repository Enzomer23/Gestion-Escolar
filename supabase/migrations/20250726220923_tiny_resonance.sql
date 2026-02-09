-- =====================================================
-- GESJ - Sistema de Gestión Educativa
-- Base de Datos Completa - Un Solo Archivo
-- Provincia de San Juan, República Argentina
-- =====================================================

-- Crear y usar la base de datos
CREATE DATABASE IF NOT EXISTS gestion_escolar;
USE gestion_escolar;

-- =====================================================
-- TABLA DE USUARIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('Padre','Docente','Preceptor','Administrativo') NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =====================================================
-- TABLA DE ALUMNOS
-- =====================================================
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE,
    fecha_nacimiento DATE,
    curso VARCHAR(20) NOT NULL,
    division VARCHAR(10) DEFAULT 'A',
    fecha_ingreso DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN DEFAULT TRUE,
    padre_id INT,
    FOREIGN KEY (padre_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_curso (curso),
    INDEX idx_activo (activo),
    INDEX idx_padre (padre_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =====================================================
-- TABLA DE MATERIAS
-- =====================================================
CREATE TABLE IF NOT EXISTS materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE,
    curso VARCHAR(20) NOT NULL,
    division VARCHAR(10) DEFAULT 'A',
    docente_id INT,
    horas_semanales INT DEFAULT 3,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (docente_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_curso_division (curso, division),
    INDEX idx_docente (docente_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =====================================================
-- TABLA DE PERÍODOS DE EVALUACIÓN
-- =====================================================
CREATE TABLE IF NOT EXISTS periodos_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    ano_lectivo YEAR NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_ano_lectivo (ano_lectivo),
    INDEX idx_fechas (fecha_inicio, fecha_fin)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =====================================================
-- TABLA DE TIPOS DE EVALUACIÓN
-- =====================================================
CREATE TABLE IF NOT EXISTS tipos_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    peso_porcentual DECIMAL(5,2) DEFAULT 100.00,
    activo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =====================================================
-- TABLA PRINCIPAL DE CALIFICACIONES
-- =====================================================
CREATE TABLE IF NOT EXISTS calificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    materia_id INT NOT NULL,
    docente_id INT NOT NULL,
    periodo_id INT NOT NULL,
    tipo_evaluacion_id INT NOT NULL,
    nota DECIMAL(4,2) NOT NULL CHECK (nota >= 1.00 AND nota <= 10.00),
    fecha_evaluacion DATE NOT NULL,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
    FOREIGN KEY (docente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (periodo_id) REFERENCES periodos_evaluacion(id) ON DELETE CASCADE,
    FOREIGN KEY (tipo_evaluacion_id) REFERENCES tipos_evaluacion(id) ON DELETE CASCADE,
    UNIQUE KEY unique_calificacion (alumno_id, materia_id, periodo_id, tipo_evaluacion_id, fecha_evaluacion),
    INDEX idx_alumno_materia (alumno_id, materia_id),
    INDEX idx_docente_periodo (docente_id, periodo_id),
    INDEX idx_fecha_evaluacion (fecha_evaluacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =====================================================
-- TABLA DE PROMEDIOS CALCULADOS (OPTIMIZACIÓN)
-- =====================================================
CREATE TABLE IF NOT EXISTS promedios_alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    materia_id INT NOT NULL,
    periodo_id INT NOT NULL,
    promedio DECIMAL(4,2) NOT NULL,
    cantidad_notas INT NOT NULL,
    nota_minima DECIMAL(4,2),
    nota_maxima DECIMAL(4,2),
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
    FOREIGN KEY (periodo_id) REFERENCES periodos_evaluacion(id) ON DELETE CASCADE,
    UNIQUE KEY unique_promedio (alumno_id, materia_id, periodo_id),
    INDEX idx_alumno_periodo (alumno_id, periodo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =====================================================
-- INSERTAR DATOS DE EJEMPLO
-- =====================================================

-- Usuarios de ejemplo
INSERT IGNORE INTO usuarios (nombre_usuario, contrasena, tipo_usuario) VALUES
('padre1', '1234', 'Padre'),
('docente1', 'abcd', 'Docente'),
('preceptor1', '5678', 'Preceptor'),
('admin1', 'adminpass', 'Administrativo'),
('padre2', '1234', 'Padre'),
('docente2', 'abcd', 'Docente'),
('preceptor2', '5678', 'Preceptor');

-- Períodos de evaluación
INSERT IGNORE INTO periodos_evaluacion (nombre, descripcion, fecha_inicio, fecha_fin, ano_lectivo) VALUES
('Primer Cuatrimestre 2025', 'Primer período de evaluación del año lectivo 2025', '2025-03-01', '2025-07-15', 2025),
('Segundo Cuatrimestre 2025', 'Segundo período de evaluación del año lectivo 2025', '2025-08-01', '2025-12-15', 2025),
('Primer Cuatrimestre 2024', 'Primer período de evaluación del año lectivo 2024', '2024-03-01', '2024-07-15', 2024);

-- Tipos de evaluación
INSERT IGNORE INTO tipos_evaluacion (nombre, descripcion, peso_porcentual) VALUES
('Evaluación Diaria', 'Evaluaciones y participación en clase', 30.00),
('Evaluación Mensual', 'Exámenes mensuales', 40.00),
('Evaluación Cuatrimestral', 'Examen final del cuatrimestre', 30.00),
('Evaluación Integradora', 'Evaluación integradora de contenidos', 25.00),
('Trabajo Práctico', 'Trabajos prácticos y proyectos', 20.00);

-- Alumnos de ejemplo
INSERT IGNORE INTO alumnos (nombre, apellido, dni, fecha_nacimiento, curso, division, padre_id) VALUES
('Juan', 'Pérez', '12345678', '2010-05-15', '1º Año', 'A', 1),
('Ana', 'Gómez', '87654321', '2009-08-22', '2º Año', 'A', 1),
('Carlos', 'Martínez', '11223344', '2008-12-10', '3º Año', 'A', 5),
('Laura', 'Díaz', '44332211', '2010-03-18', '1º Año', 'A', 1),
('Mario', 'González', '55667788', '2009-11-05', '2º Año', 'A', 5),
('Sofía', 'Ramírez', '99887766', '2008-07-30', '3º Año', 'A', 1),
('Pedro', 'Rodríguez', '13579246', '2010-01-25', '1º Año', 'B', 5),
('María', 'Fernández', '24681357', '2009-09-12', '2º Año', 'B', 1),
('Lucas', 'Herrera', '36925814', '2008-04-08', '3º Año', 'B', 5),
('Julia', 'Castro', '14725836', '2010-06-20', '1º Año', 'B', 1),
('Diego', 'López', '25814736', '2010-02-14', '1º Año', 'A', 5),
('Valentina', 'Morales', '36925847', '2009-10-30', '2º Año', 'A', 1);

-- Materias de ejemplo
INSERT IGNORE INTO materias (nombre, codigo, curso, division, docente_id, horas_semanales) VALUES
-- 1º Año A
('Matemáticas', 'MAT1A', '1º Año', 'A', 2, 5),
('Lengua y Literatura', 'LEN1A', '1º Año', 'A', 2, 4),
('Ciencias Naturales', 'CNA1A', '1º Año', 'A', 6, 3),
('Historia', 'HIS1A', '1º Año', 'A', 2, 3),
('Geografía', 'GEO1A', '1º Año', 'A', 6, 2),
('Educación Física', 'EDF1A', '1º Año', 'A', 6, 2),
-- 1º Año B
('Matemáticas', 'MAT1B', '1º Año', 'B', 6, 5),
('Lengua y Literatura', 'LEN1B', '1º Año', 'B', 6, 4),
('Ciencias Naturales', 'CNA1B', '1º Año', 'B', 2, 3),
-- 2º Año A
('Matemáticas', 'MAT2A', '2º Año', 'A', 2, 5),
('Lengua y Literatura', 'LEN2A', '2º Año', 'A', 6, 4),
('Física', 'FIS2A', '2º Año', 'A', 2, 3),
('Química', 'QUI2A', '2º Año', 'A', 6, 3),
('Biología', 'BIO2A', '2º Año', 'A', 2, 3),
('Historia', 'HIS2A', '2º Año', 'A', 6, 3),
-- 2º Año B
('Matemáticas', 'MAT2B', '2º Año', 'B', 6, 5),
('Física', 'FIS2B', '2º Año', 'B', 6, 3),
-- 3º Año A
('Matemáticas', 'MAT3A', '3º Año', 'A', 2, 5),
('Física', 'FIS3A', '3º Año', 'A', 6, 4),
('Química', 'QUI3A', '3º Año', 'A', 2, 4),
-- 3º Año B
('Matemáticas', 'MAT3B', '3º Año', 'B', 6, 5),
('Física', 'FIS3B', '3º Año', 'B', 2, 4);

-- Calificaciones de ejemplo (datos realistas)
INSERT IGNORE INTO calificaciones (alumno_id, materia_id, docente_id, periodo_id, tipo_evaluacion_id, nota, fecha_evaluacion, observaciones) VALUES
-- Juan Pérez (ID: 1) - 1º Año A
(1, 1, 2, 1, 1, 8.50, '2025-03-15', 'Buen desempeño en clase'),
(1, 1, 2, 1, 2, 7.75, '2025-04-10', 'Examen mensual satisfactorio'),
(1, 1, 2, 1, 3, 8.00, '2025-07-10', 'Examen final aprobado'),
(1, 2, 2, 1, 1, 9.00, '2025-03-18', 'Excelente comprensión lectora'),
(1, 2, 2, 1, 2, 8.25, '2025-04-12', 'Muy buena expresión escrita'),
(1, 2, 2, 1, 3, 8.75, '2025-07-11', 'Destacado en literatura'),

-- Ana Gómez (ID: 2) - 2º Año A
(2, 10, 2, 1, 1, 9.00, '2025-03-20', 'Excelente participación'),
(2, 10, 2, 1, 2, 8.25, '2025-04-15', 'Muy buen rendimiento'),
(2, 10, 2, 1, 3, 8.75, '2025-07-12', 'Examen final destacado'),
(2, 11, 6, 1, 1, 8.50, '2025-03-22', 'Buena comprensión'),
(2, 11, 6, 1, 2, 9.00, '2025-04-18', 'Excelente redacción'),

-- Carlos Martínez (ID: 3) - 3º Año A
(3, 18, 2, 1, 1, 7.00, '2025-03-25', 'Necesita refuerzo'),
(3, 18, 2, 1, 2, 6.50, '2025-04-20', 'Mejorando gradualmente'),
(3, 18, 2, 1, 3, 7.25, '2025-07-14', 'Logró aprobar'),
(3, 19, 6, 1, 1, 6.75, '2025-03-28', 'Dificultades con conceptos'),
(3, 19, 6, 1, 2, 7.00, '2025-04-22', 'Mejora notable'),

-- Laura Díaz (ID: 4) - 1º Año A
(4, 1, 2, 1, 1, 9.25, '2025-03-16', 'Excelente alumna'),
(4, 1, 2, 1, 2, 8.75, '2025-04-11', 'Muy buen rendimiento'),
(4, 1, 2, 1, 3, 9.00, '2025-07-09', 'Sobresaliente'),
(4, 2, 2, 1, 1, 9.50, '2025-03-19', 'Destacada en lengua'),
(4, 2, 2, 1, 2, 9.00, '2025-04-13', 'Excelente expresión'),

-- Mario González (ID: 5) - 2º Año A - ALUMNO EN RIESGO
(5, 10, 2, 1, 1, 6.00, '2025-03-21', 'Dificultades con álgebra'),
(5, 10, 2, 1, 2, 5.75, '2025-04-16', 'Necesita apoyo adicional'),
(5, 10, 2, 1, 3, 6.25, '2025-07-13', 'Logró aprobar con esfuerzo'),
(5, 12, 2, 1, 1, 5.50, '2025-03-23', 'Conceptos básicos débiles'),
(5, 12, 2, 1, 2, 6.00, '2025-04-19', 'Leve mejora'),

-- Sofía Ramírez (ID: 6) - 3º Año A
(6, 18, 2, 1, 1, 8.75, '2025-03-26', 'Muy buena alumna'),
(6, 18, 2, 1, 2, 8.50, '2025-04-21', 'Constante en su rendimiento'),
(6, 18, 2, 1, 3, 8.25, '2025-07-15', 'Buen desempeño final'),

-- Pedro Rodríguez (ID: 7) - 1º Año B - ALUMNO EN RIESGO
(7, 7, 6, 1, 1, 5.50, '2025-03-17', 'Dificultades importantes'),
(7, 7, 6, 1, 2, 5.25, '2025-04-14', 'Requiere refuerzo urgente'),
(7, 7, 6, 1, 3, 5.75, '2025-07-08', 'Aprobó por poco'),

-- María Fernández (ID: 8) - 2º Año B
(8, 16, 6, 1, 1, 8.00, '2025-03-24', 'Buen nivel'),
(8, 16, 6, 1, 2, 7.75, '2025-04-17', 'Mantiene el ritmo'),
(8, 16, 6, 1, 3, 8.25, '2025-07-16', 'Mejora continua'),

-- Lucas Herrera (ID: 9) - 3º Año B - ALUMNO EN RIESGO CRÍTICO
(9, 21, 6, 1, 1, 4.50, '2025-03-27', 'Serias dificultades'),
(9, 21, 6, 1, 2, 5.00, '2025-04-23', 'Leve mejora insuficiente'),
(9, 21, 6, 1, 3, 5.25, '2025-07-17', 'Necesita recuperatorio'),

-- Julia Castro (ID: 10) - 1º Año B
(10, 7, 6, 1, 1, 8.25, '2025-03-18', 'Muy buena estudiante'),
(10, 7, 6, 1, 2, 8.50, '2025-04-15', 'Excelente progreso'),
(10, 7, 6, 1, 3, 8.75, '2025-07-12', 'Destacada performance');

-- =====================================================
-- VISTAS PARA CONSULTAS OPTIMIZADAS
-- =====================================================

-- Vista para consultas rápidas de calificaciones
CREATE OR REPLACE VIEW vista_calificaciones AS
SELECT 
    c.id,
    c.alumno_id,
    c.materia_id,
    c.periodo_id,
    c.tipo_evaluacion_id,
    CONCAT(a.apellido, ', ', a.nombre) AS alumno,
    a.curso,
    a.division,
    m.nombre AS materia,
    m.codigo AS codigo_materia,
    u.nombre_usuario AS docente,
    p.nombre AS periodo,
    te.nombre AS tipo_evaluacion,
    c.nota,
    c.fecha_evaluacion,
    c.observaciones,
    c.fecha_registro
FROM calificaciones c
JOIN alumnos a ON c.alumno_id = a.id
JOIN materias m ON c.materia_id = m.id
JOIN usuarios u ON c.docente_id = u.id
JOIN periodos_evaluacion p ON c.periodo_id = p.id
JOIN tipos_evaluacion te ON c.tipo_evaluacion_id = te.id
WHERE a.activo = TRUE AND m.activa = TRUE
ORDER BY a.apellido, a.nombre, m.nombre, c.fecha_evaluacion;

-- Vista para promedios por alumno y materia
CREATE OR REPLACE VIEW vista_promedios AS
SELECT 
    a.id AS alumno_id,
    CONCAT(a.apellido, ', ', a.nombre) AS alumno,
    a.curso,
    a.division,
    m.id AS materia_id,
    m.nombre AS materia,
    p.id AS periodo_id,
    p.nombre AS periodo,
    ROUND(AVG(c.nota), 2) AS promedio,
    COUNT(c.nota) AS cantidad_notas,
    MIN(c.nota) AS nota_minima,
    MAX(c.nota) AS nota_maxima
FROM calificaciones c
JOIN alumnos a ON c.alumno_id = a.id
JOIN materias m ON c.materia_id = m.id
JOIN periodos_evaluacion p ON c.periodo_id = p.id
WHERE a.activo = TRUE AND m.activa = TRUE
GROUP BY a.id, m.id, p.id
ORDER BY a.apellido, a.nombre, m.nombre;

-- Vista para alumnos en riesgo académico
CREATE OR REPLACE VIEW vista_alumnos_riesgo AS
SELECT 
    a.id AS alumno_id,
    CONCAT(a.apellido, ', ', a.nombre) AS alumno,
    a.curso,
    a.division,
    p.id AS periodo_id,
    p.nombre AS periodo,
    ROUND(AVG(c.nota), 2) AS promedio_general,
    COUNT(DISTINCT m.id) AS materias_cursadas,
    COUNT(c.nota) AS total_calificaciones,
    CASE 
        WHEN AVG(c.nota) < 5.0 THEN 'CRÍTICO'
        WHEN AVG(c.nota) < 6.0 THEN 'ALTO'
        WHEN AVG(c.nota) < 7.0 THEN 'MODERADO'
        ELSE 'BAJO'
    END AS nivel_riesgo
FROM calificaciones c
JOIN alumnos a ON c.alumno_id = a.id
JOIN materias m ON c.materia_id = m.id
JOIN periodos_evaluacion p ON c.periodo_id = p.id
WHERE a.activo = TRUE AND m.activa = TRUE
GROUP BY a.id, p.id
HAVING promedio_general < 7.0
ORDER BY promedio_general ASC;

-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS
-- =====================================================

-- Procedimiento para calcular y actualizar promedios
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS CalcularPromedios()
BEGIN
    -- Limpiar tabla de promedios
    DELETE FROM promedios_alumnos;
    
    -- Insertar promedios calculados
    INSERT INTO promedios_alumnos (alumno_id, materia_id, periodo_id, promedio, cantidad_notas, nota_minima, nota_maxima)
    SELECT 
        alumno_id,
        materia_id,
        periodo_id,
        ROUND(AVG(nota), 2) as promedio,
        COUNT(*) as cantidad_notas,
        MIN(nota) as nota_minima,
        MAX(nota) as nota_maxima
    FROM calificaciones
    GROUP BY alumno_id, materia_id, periodo_id;
    
    SELECT CONCAT('Promedios actualizados: ', ROW_COUNT(), ' registros') AS resultado;
END //
DELIMITER ;

-- Procedimiento para obtener estadísticas de un curso
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS EstadisticasCurso(IN p_curso VARCHAR(20), IN p_division VARCHAR(10), IN p_periodo_id INT)
BEGIN
    SELECT 
        'Estadísticas del Curso' AS tipo,
        p_curso AS curso,
        p_division AS division,
        COUNT(DISTINCT a.id) as total_alumnos,
        COUNT(DISTINCT m.id) as total_materias,
        ROUND(AVG(c.nota), 2) as promedio_curso,
        COUNT(c.id) as total_calificaciones,
        COUNT(CASE WHEN c.nota >= 6.0 THEN 1 END) as notas_aprobadas,
        COUNT(CASE WHEN c.nota < 6.0 THEN 1 END) as notas_desaprobadas
    FROM alumnos a
    LEFT JOIN calificaciones c ON a.id = c.alumno_id AND c.periodo_id = p_periodo_id
    LEFT JOIN materias m ON c.materia_id = m.id
    WHERE a.curso = p_curso AND a.division = p_division AND a.activo = TRUE;
END //
DELIMITER ;

-- =====================================================
-- FUNCIONES ÚTILES
-- =====================================================

-- Función para obtener el promedio general de un alumno
DELIMITER //
CREATE FUNCTION IF NOT EXISTS PromedioGeneralAlumno(p_alumno_id INT, p_periodo_id INT) 
RETURNS DECIMAL(4,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE promedio_general DECIMAL(4,2);
    
    SELECT ROUND(AVG(nota), 2) INTO promedio_general
    FROM calificaciones
    WHERE alumno_id = p_alumno_id AND periodo_id = p_periodo_id;
    
    RETURN IFNULL(promedio_general, 0.00);
END //
DELIMITER ;

-- Función para determinar el estado académico de un alumno
DELIMITER //
CREATE FUNCTION IF NOT EXISTS EstadoAcademicoAlumno(p_promedio DECIMAL(4,2)) 
RETURNS VARCHAR(20)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE estado VARCHAR(20);
    
    CASE 
        WHEN p_promedio >= 9.0 THEN SET estado = 'EXCELENTE';
        WHEN p_promedio >= 8.0 THEN SET estado = 'MUY BUENO';
        WHEN p_promedio >= 7.0 THEN SET estado = 'BUENO';
        WHEN p_promedio >= 6.0 THEN SET estado = 'REGULAR';
        WHEN p_promedio >= 4.0 THEN SET estado = 'EN RIESGO';
        ELSE SET estado = 'CRÍTICO';
    END CASE;
    
    RETURN estado;
END //
DELIMITER ;

-- =====================================================
-- TRIGGERS PARA AUDITORÍA Y AUTOMATIZACIÓN
-- =====================================================

-- Trigger para actualizar promedios automáticamente
DELIMITER //
CREATE TRIGGER IF NOT EXISTS actualizar_promedio_after_insert
AFTER INSERT ON calificaciones
FOR EACH ROW
BEGIN
    -- Actualizar o insertar promedio
    INSERT INTO promedios_alumnos (alumno_id, materia_id, periodo_id, promedio, cantidad_notas, nota_minima, nota_maxima)
    SELECT 
        NEW.alumno_id,
        NEW.materia_id,
        NEW.periodo_id,
        ROUND(AVG(nota), 2),
        COUNT(*),
        MIN(nota),
        MAX(nota)
    FROM calificaciones 
    WHERE alumno_id = NEW.alumno_id AND materia_id = NEW.materia_id AND periodo_id = NEW.periodo_id
    ON DUPLICATE KEY UPDATE
        promedio = VALUES(promedio),
        cantidad_notas = VALUES(cantidad_notas),
        nota_minima = VALUES(nota_minima),
        nota_maxima = VALUES(nota_maxima),
        fecha_calculo = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- =====================================================
-- EJECUTAR CÁLCULOS INICIALES
-- =====================================================

-- Calcular promedios iniciales
CALL CalcularPromedios();

-- =====================================================
-- CONSULTAS DE VERIFICACIÓN
-- =====================================================

-- Verificar que todo esté funcionando
SELECT 'VERIFICACIÓN DEL SISTEMA' AS mensaje;
SELECT COUNT(*) as total_usuarios FROM usuarios;
SELECT COUNT(*) as total_alumnos FROM alumnos;
SELECT COUNT(*) as total_materias FROM materias;
SELECT COUNT(*) as total_calificaciones FROM calificaciones;
SELECT COUNT(*) as total_promedios FROM promedios_alumnos;

-- Mostrar algunos datos de ejemplo
SELECT 'USUARIOS DE PRUEBA' AS mensaje;
SELECT nombre_usuario, tipo_usuario FROM usuarios ORDER BY tipo_usuario;

SELECT 'ALUMNOS EN RIESGO' AS mensaje;
SELECT alumno, curso, division, promedio_general, nivel_riesgo 
FROM vista_alumnos_riesgo 
ORDER BY promedio_general ASC;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
SELECT '¡BASE DE DATOS GESJ CREADA EXITOSAMENTE!' AS mensaje;
SELECT 'Usuarios disponibles: padre1/1234, docente1/abcd, preceptor1/5678, admin1/adminpass' AS credenciales;