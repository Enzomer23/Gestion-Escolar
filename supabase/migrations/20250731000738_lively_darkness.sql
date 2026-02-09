-- =====================================================
-- CREAR TABLA PROMEDIOS_ALUMNOS SIMPLE
-- GESJ - Sistema de Gestión Educativa
-- =====================================================

USE gestion_escolar;

-- Eliminar tabla si existe (para recrearla limpia)
DROP TABLE IF EXISTS promedios_alumnos;

-- Crear tabla promedios_alumnos SIMPLE (sin columnas problemáticas)
CREATE TABLE promedios_alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    materia_id INT NOT NULL,
    periodo_id INT NOT NULL,
    promedio DECIMAL(4,2) NOT NULL,
    cantidad_notas INT NOT NULL,
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
    FOREIGN KEY (periodo_id) REFERENCES periodos_evaluacion(id) ON DELETE CASCADE,
    UNIQUE KEY unique_promedio (alumno_id, materia_id, periodo_id),
    INDEX idx_alumno_periodo (alumno_id, periodo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Calcular promedios iniciales
INSERT INTO promedios_alumnos (alumno_id, materia_id, periodo_id, promedio, cantidad_notas)
SELECT 
    alumno_id,
    materia_id,
    periodo_id,
    ROUND(AVG(nota), 2) as promedio,
    COUNT(*) as cantidad_notas
FROM calificaciones
GROUP BY alumno_id, materia_id, periodo_id;

-- Verificar que se creó correctamente
SELECT 'TABLA PROMEDIOS_ALUMNOS CREADA CORRECTAMENTE' AS mensaje;
SELECT COUNT(*) as total_promedios FROM promedios_alumnos;
SELECT 'ESTRUCTURA DE LA TABLA:' AS info;
DESCRIBE promedios_alumnos;