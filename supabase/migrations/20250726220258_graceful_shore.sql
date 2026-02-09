/*
# Sistema de Gestión de Calificaciones - GESJ
# Provincia de San Juan, República Argentina

1. Nuevas Tablas
   - `alumnos`: Información básica de estudiantes
   - `materias`: Materias por curso y docente
   - `calificaciones`: Notas de los alumnos por materia
   - `periodos_evaluacion`: Períodos académicos (cuatrimestres, etc.)
   - `tipos_evaluacion`: Tipos de evaluación (diaria, mensual, final, etc.)
   - `promedios_alumnos`: Tabla optimizada para cálculos de promedios

2. Relaciones
   - Alumnos pueden tener múltiples calificaciones
   - Materias están asignadas a docentes específicos
   - Calificaciones están vinculadas a períodos y tipos de evaluación

3. Funcionalidades
   - Registro de notas por período
   - Cálculo automático de promedios
   - Seguimiento histórico de calificaciones
   - Reportes por alumno, materia y período
   - Identificación de alumnos en riesgo académico
*/

-- Usar la base de datos existente
USE gestion_escolar;

-- Tabla de alumnos
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
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla de materias
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

-- Tabla de períodos de evaluación
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

-- Tabla de tipos de evaluación
CREATE TABLE IF NOT EXISTS tipos_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    peso_porcentual DECIMAL(5,2) DEFAULT 100.00,
    activo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla principal de calificaciones
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

-- Tabla para promedios calculados (para optimización)
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

-- Insertar datos de ejemplo

-- Períodos de evaluación
INSERT IGNORE INTO periodos_evaluacion (nombre, descripcion, fecha_inicio, fecha_fin, ano_lectivo) VALUES
('Primer Cuatrimestre 2025', 'Primer período de evaluación del año lectivo 2025', '2025-03-01', '2025-07-15', 2025),
('Segundo Cuatrimestre 2025', 'Segundo período de evaluación del año lectivo 2025', '2025-08-01', '2025-12-15', 2025);

-- Tipos de evaluación
INSERT IGNORE INTO tipos_evaluacion (nombre, descripcion, peso_porcentual) VALUES
('Evaluación Diaria', 'Evaluaciones y participación en clase', 30.00),
('Evaluación Mensual', 'Exámenes mensuales', 40.00),
('Evaluación Cuatrimestral', 'Examen final del cuatrimestre', 30.00);

-- Alumnos de ejemplo
INSERT IGNORE INTO alumnos (nombre, apellido, dni, fecha_nacimiento, curso, division, padre_id) VALUES
('Juan', 'Pérez', '12345678', '2010-05-15', '1º Año', 'A', 1),
('Ana', 'Gómez', '87654321', '2009-08-22', '2º Año', 'A', 1),
('Carlos', 'Martínez', '11223344', '2008-12-10', '3º Año', 'A', 1),
('Laura', 'Díaz', '44332211', '2010-03-18', '1º Año', 'A', 1),
('Mario', 'González', '55667788', '2009-11-05', '2º Año', 'A', 1),
('Sofía', 'Ramírez', '99887766', '2008-07-30', '3º Año', 'A', 1),
('Pedro', 'Rodríguez', '13579246', '2010-01-25', '1º Año', 'B', 1),
('María', 'Fernández', '24681357', '2009-09-12', '2º Año', 'B', 1),
('Lucas', 'Herrera', '36925814', '2008-04-08', '3º Año', 'B', 1),
('Julia', 'Castro', '14725836', '2010-06-20', '1º Año', 'B', 1);

-- Materias de ejemplo
INSERT IGNORE INTO materias (nombre, codigo, curso, division, docente_id, horas_semanales) VALUES
('Matemáticas', 'MAT1A', '1º Año', 'A', 2, 5),
('Lengua y Literatura', 'LEN1A', '1º Año', 'A', 2, 4),
('Ciencias Naturales', 'CNA1A', '1º Año', 'A', 2, 3),
('Historia', 'HIS1A', '1º Año', 'A', 2, 3),
('Geografía', 'GEO1A', '1º Año', 'A', 2, 2),
('Matemáticas', 'MAT2A', '2º Año', 'A', 2, 5),
('Lengua y Literatura', 'LEN2A', '2º Año', 'A', 2, 4),
('Física', 'FIS2A', '2º Año', 'A', 2, 3),
('Química', 'QUI2A', '2º Año', 'A', 2, 3),
('Biología', 'BIO2A', '2º Año', 'A', 2, 3);

-- Calificaciones de ejemplo
INSERT IGNORE INTO calificaciones (alumno_id, materia_id, docente_id, periodo_id, tipo_evaluacion_id, nota, fecha_evaluacion, observaciones) VALUES
-- Juan Pérez - Matemáticas
(1, 1, 2, 1, 1, 8.50, '2025-03-15', 'Buen desempeño en clase'),
(1, 1, 2, 1, 2, 7.75, '2025-04-10', 'Examen mensual satisfactorio'),
(1, 1, 2, 1, 3, 8.00, '2025-07-10', 'Examen final aprobado'),
-- Ana Gómez - Matemáticas 2º Año
(2, 6, 2, 1, 1, 9.00, '2025-03-20', 'Excelente participación'),
(2, 6, 2, 1, 2, 8.25, '2025-04-15', 'Muy buen rendimiento'),
(2, 6, 2, 1, 3, 8.75, '2025-07-12', 'Examen final destacado'),
-- Carlos Martínez - Física
(3, 8, 2, 1, 1, 7.00, '2025-03-25', 'Necesita refuerzo'),
(3, 8, 2, 1, 2, 6.50, '2025-04-20', 'Mejorando gradualmente'),
(3, 8, 2, 1, 3, 7.25, '2025-07-14', 'Logró aprobar'),
-- Laura Díaz - Lengua y Literatura
(4, 2, 2, 1, 1, 9.25, '2025-03-18', 'Excelente comprensión lectora'),
(4, 2, 2, 1, 2, 8.50, '2025-04-12', 'Muy buena expresión escrita'),
(4, 2, 2, 1, 3, 9.00, '2025-07-11', 'Destacada en literatura'),
-- Mario González - Matemáticas 2º Año
(5, 6, 2, 1, 1, 6.00, '2025-03-22', 'Dificultades con álgebra'),
(5, 6, 2, 1, 2, 5.75, '2025-04-18', 'Necesita apoyo adicional'),
(5, 6, 2, 1, 3, 6.25, '2025-07-13', 'Logró aprobar con esfuerzo');

-- Vista para consultas rápidas de calificaciones
CREATE OR REPLACE VIEW vista_calificaciones AS
SELECT 
    c.id,
    c.alumno_id,
    c.materia_id,
    c.periodo_id,
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
END //
DELIMITER ;

-- Función para obtener el promedio general de un alumno
DELIMITER //
CREATE FUNCTION IF NOT EXISTS PromedioGeneralAlumno(p_alumno_id INT, p_periodo_id INT) 
RETURNS DECIMAL(4,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE promedio_general DECIMAL(4,2);
    
    SELECT ROUND(AVG(promedio), 2) INTO promedio_general
    FROM promedios_alumnos
    WHERE alumno_id = p_alumno_id AND periodo_id = p_periodo_id;
    
    RETURN IFNULL(promedio_general, 0.00);
END //
DELIMITER ;

-- Ejecutar cálculo inicial de promedios
CALL CalcularPromedios();