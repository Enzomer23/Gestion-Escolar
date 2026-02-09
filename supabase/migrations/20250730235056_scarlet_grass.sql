-- =====================================================
-- AGREGAR MÁS ALUMNOS A LA BASE DE DATOS GESJ
-- Provincia de San Juan, República Argentina
-- =====================================================

USE gestion_escolar;

-- =====================================================
-- NUEVOS ALUMNOS PARA 1º AÑO A
-- =====================================================
INSERT IGNORE INTO alumnos (nombre, apellido, dni, fecha_nacimiento, curso, division, padre_id) VALUES
('Mateo', 'Silva', '15975346', '2010-04-12', '1º Año', 'A', 1),
('Camila', 'Torres', '26841357', '2010-07-08', '1º Año', 'A', 5),
('Nicolás', 'Vega', '37159264', '2010-01-22', '1º Año', 'A', 1),
('Isabella', 'Moreno', '48263175', '2010-09-15', '1º Año', 'A', 5),
('Santiago', 'Ruiz', '59374286', '2010-03-30', '1º Año', 'A', 1);

-- =====================================================
-- NUEVOS ALUMNOS PARA 1º AÑO B
-- =====================================================
INSERT IGNORE INTO alumnos (nombre, apellido, dni, fecha_nacimiento, curso, division, padre_id) VALUES
('Valentino', 'Acosta', '61485397', '2010-06-18', '1º Año', 'B', 5),
('Martina', 'Jiménez', '72596408', '2010-11-03', '1º Año', 'B', 1),
('Thiago', 'Mendoza', '83607519', '2010-02-27', '1º Año', 'B', 5),
('Renata', 'Cabrera', '94718620', '2010-08-14', '1º Año', 'B', 1),
('Benjamín', 'Vargas', '15829731', '2010-05-09', '1º Año', 'B', 5);

-- =====================================================
-- NUEVOS ALUMNOS PARA 2º AÑO A
-- =====================================================
INSERT IGNORE INTO alumnos (nombre, apellido, dni, fecha_nacimiento, curso, division, padre_id) VALUES
('Emilia', 'Sánchez', '26940842', '2009-03-16', '2º Año', 'A', 1),
('Joaquín', 'Romero', '38051953', '2009-10-21', '2º Año', 'A', 5),
('Catalina', 'Guerrero', '49162064', '2009-01-07', '2º Año', 'A', 1),
('Agustín', 'Medina', '50273175', '2009-07-25', '2º Año', 'A', 5),
('Delfina', 'Ortega', '61384286', '2009-12-11', '2º Año', 'A', 1);

-- =====================================================
-- NUEVOS ALUMNOS PARA 2º AÑO B
-- =====================================================
INSERT IGNORE INTO alumnos (nombre, apellido, dni, fecha_nacimiento, curso, division, padre_id) VALUES
('Tomás', 'Navarro', '72495397', '2009-04-02', '2º Año', 'B', 5),
('Julieta', 'Peña', '83506408', '2009-09-28', '2º Año', 'B', 1),
('Máximo', 'Herrera', '94617519', '2009-02-14', '2º Año', 'B', 5),
('Amparo', 'Molina', '15728630', '2009-08-06', '2º Año', 'B', 1),
('Bautista', 'Ramos', '26839741', '2009-11-19', '2º Año', 'B', 5);

-- =====================================================
-- NUEVOS ALUMNOS PARA 3º AÑO A
-- =====================================================
INSERT IGNORE INTO alumnos (nombre, apellido, dni, fecha_nacimiento, curso, division, padre_id) VALUES
('Mía', 'Flores', '37940852', '2008-05-13', '3º Año', 'A', 1),
('Lautaro', 'Aguilar', '48051963', '2008-12-08', '3º Año', 'A', 5),
('Pilar', 'Cortés', '59162074', '2008-03-24', '3º Año', 'A', 1),
('Facundo', 'Ríos', '60273185', '2008-10-17', '3º Año', 'A', 5),
('Alma', 'Paredes', '71384296', '2008-01-31', '3º Año', 'A', 1);

-- =====================================================
-- NUEVOS ALUMNOS PARA 3º AÑO B
-- =====================================================
INSERT IGNORE INTO alumnos (nombre, apellido, dni, fecha_nacimiento, curso, division, padre_id) VALUES
('Gael', 'Domínguez', '82495307', '2008-06-20', '3º Año', 'B', 5),
('Zoe', 'Castro', '93506418', '2008-11-05', '3º Año', 'B', 1),
('Ian', 'Morales', '14617529', '2008-04-12', '3º Año', 'B', 5),
('Abril', 'Vázquez', '25728640', '2008-09-26', '3º Año', 'B', 1),
('Dante', 'Figueroa', '36839751', '2008-02-18', '3º Año', 'B', 5);

-- =====================================================
-- CALIFICACIONES DE EJEMPLO PARA ALGUNOS NUEVOS ALUMNOS
-- =====================================================

-- Mateo Silva (ID será el siguiente disponible) - 1º Año A - Buen alumno
INSERT IGNORE INTO calificaciones (alumno_id, materia_id, docente_id, periodo_id, tipo_evaluacion_id, nota, fecha_evaluacion, observaciones) VALUES
-- Necesitaremos los IDs reales después de la inserción
-- Por ahora dejamos algunos ejemplos comentados:

/*
-- Ejemplo para cuando sepamos los IDs:
(13, 1, 2, 1, 1, 8.25, '2025-03-17', 'Muy buen desempeño'),
(13, 1, 2, 1, 2, 7.50, '2025-04-14', 'Sólido rendimiento'),
(13, 2, 2, 1, 1, 8.75, '2025-03-19', 'Excelente en lengua'),
*/

-- =====================================================
-- CONSULTAS PARA VERIFICAR LOS NUEVOS ALUMNOS
-- =====================================================

-- Ver todos los alumnos por curso
SELECT 'RESUMEN POR CURSO' AS info;
SELECT curso, division, COUNT(*) as total_alumnos 
FROM alumnos 
WHERE activo = TRUE 
GROUP BY curso, division 
ORDER BY curso, division;

-- Ver los nuevos alumnos agregados
SELECT 'NUEVOS ALUMNOS AGREGADOS' AS info;
SELECT CONCAT(apellido, ', ', nombre) as alumno, curso, division, dni, fecha_nacimiento
FROM alumnos 
WHERE id > 12  -- Los primeros 12 ya existían
ORDER BY curso, division, apellido;

-- Estadísticas generales
SELECT 'ESTADÍSTICAS GENERALES' AS info;
SELECT 
    COUNT(*) as total_alumnos,
    COUNT(CASE WHEN curso = '1º Año' THEN 1 END) as primer_año,
    COUNT(CASE WHEN curso = '2º Año' THEN 1 END) as segundo_año,
    COUNT(CASE WHEN curso = '3º Año' THEN 1 END) as tercer_año
FROM alumnos 
WHERE activo = TRUE;

-- =====================================================
-- SCRIPT PARA AGREGAR CALIFICACIONES A LOS NUEVOS ALUMNOS
-- (Ejecutar después de verificar los IDs)
-- =====================================================

/*
-- Plantilla para agregar calificaciones:
-- 1. Primero ejecutar este archivo
-- 2. Verificar los IDs de los nuevos alumnos
-- 3. Usar esta plantilla para agregar calificaciones:

INSERT INTO calificaciones (alumno_id, materia_id, docente_id, periodo_id, tipo_evaluacion_id, nota, fecha_evaluacion, observaciones) VALUES
-- Para 1º Año A - Matemáticas (materia_id = 1)
(ID_ALUMNO, 1, 2, 1, 1, NOTA, 'FECHA', 'OBSERVACION'),
-- Para 1º Año A - Lengua (materia_id = 2)  
(ID_ALUMNO, 2, 2, 1, 1, NOTA, 'FECHA', 'OBSERVACION');
*/

SELECT '¡NUEVOS ALUMNOS AGREGADOS EXITOSAMENTE!' AS mensaje;