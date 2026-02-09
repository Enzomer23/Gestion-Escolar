-- =====================================================
-- LIMPIAR REFERENCIAS A nota_minima Y nota_maxima EN MYSQL
-- GESJ - Sistema de Gestión Educativa
-- =====================================================

USE gestion_escolar;

-- =====================================================
-- 1. ELIMINAR TRIGGER QUE PUEDE ESTAR CAUSANDO EL ERROR
-- =====================================================

-- Verificar si existe el trigger problemático
DROP TRIGGER IF EXISTS actualizar_promedio_after_insert;

-- =====================================================
-- 2. RECREAR TRIGGER SIN REFERENCIAS PROBLEMÁTICAS
-- =====================================================

DELIMITER //
CREATE TRIGGER actualizar_promedio_after_insert
AFTER INSERT ON calificaciones
FOR EACH ROW
BEGIN
    -- Actualizar o insertar promedio (SIN nota_minima/nota_maxima)
    INSERT INTO promedios_alumnos (alumno_id, materia_id, periodo_id, promedio, cantidad_notas)
    SELECT 
        NEW.alumno_id,
        NEW.materia_id,
        NEW.periodo_id,
        ROUND(AVG(nota), 2),
        COUNT(*)
    FROM calificaciones 
    WHERE alumno_id = NEW.alumno_id AND materia_id = NEW.materia_id AND periodo_id = NEW.periodo_id
    ON DUPLICATE KEY UPDATE
        promedio = VALUES(promedio),
        cantidad_notas = VALUES(cantidad_notas),
        fecha_calculo = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- =====================================================
-- 3. VERIFICAR QUE NO HAY PROCEDIMIENTOS PROBLEMÁTICOS
-- =====================================================

-- Eliminar procedimiento si tiene referencias problemáticas
DROP PROCEDURE IF EXISTS CalcularPromedios;

-- Recrear procedimiento limpio
DELIMITER //
CREATE PROCEDURE CalcularPromedios()
BEGIN
    -- Limpiar tabla de promedios
    DELETE FROM promedios_alumnos;
    
    -- Insertar promedios calculados (SIN nota_minima/nota_maxima)
    INSERT INTO promedios_alumnos (alumno_id, materia_id, periodo_id, promedio, cantidad_notas)
    SELECT 
        alumno_id,
        materia_id,
        periodo_id,
        ROUND(AVG(nota), 2) as promedio,
        COUNT(*) as cantidad_notas
    FROM calificaciones
    GROUP BY alumno_id, materia_id, periodo_id;
    
    SELECT CONCAT('Promedios actualizados: ', ROW_COUNT(), ' registros') AS resultado;
END //
DELIMITER ;

-- =====================================================
-- 4. VERIFICAR ESTRUCTURA DE LA TABLA
-- =====================================================

-- Mostrar estructura actual de promedios_alumnos
DESCRIBE promedios_alumnos;

-- =====================================================
-- 5. MENSAJE DE CONFIRMACIÓN
-- =====================================================

SELECT '¡BASE DE DATOS LIMPIADA! Triggers y procedimientos actualizados sin nota_minima/nota_maxima' AS mensaje;