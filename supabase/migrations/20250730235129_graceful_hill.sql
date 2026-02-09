-- =====================================================
-- CONSULTAS PARA VER Y GESTIONAR ALUMNOS
-- GESJ - Sistema de Gestión Educativa
-- =====================================================

USE gestion_escolar;

-- =====================================================
-- 1. VER TODOS LOS ALUMNOS POR CURSO
-- =====================================================
SELECT '=== ALUMNOS POR CURSO Y DIVISIÓN ===' AS info;

SELECT 
    curso,
    division,
    COUNT(*) as total_alumnos,
    GROUP_CONCAT(CONCAT(apellido, ', ', nombre) ORDER BY apellido SEPARATOR ' | ') as alumnos
FROM alumnos 
WHERE activo = TRUE 
GROUP BY curso, division 
ORDER BY curso, division;

-- =====================================================
-- 2. LISTADO COMPLETO DE ALUMNOS
-- =====================================================
SELECT '=== LISTADO COMPLETO DE ALUMNOS ===' AS info;

SELECT 
    id,
    CONCAT(apellido, ', ', nombre) as alumno,
    dni,
    DATE_FORMAT(fecha_nacimiento, '%d/%m/%Y') as fecha_nacimiento,
    CONCAT(curso, ' - ', division) as curso_division,
    TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) as edad,
    CASE 
        WHEN padre_id = 1 THEN 'padre1'
        WHEN padre_id = 5 THEN 'padre2'
        ELSE 'Sin asignar'
    END as padre_usuario
FROM alumnos 
WHERE activo = TRUE
ORDER BY curso, division, apellido, nombre;

-- =====================================================
-- 3. ESTADÍSTICAS POR CURSO
-- =====================================================
SELECT '=== ESTADÍSTICAS POR CURSO ===' AS info;

SELECT 
    curso,
    COUNT(*) as total_alumnos,
    COUNT(CASE WHEN division = 'A' THEN 1 END) as division_A,
    COUNT(CASE WHEN division = 'B' THEN 1 END) as division_B,
    ROUND(AVG(TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE())), 1) as edad_promedio
FROM alumnos 
WHERE activo = TRUE
GROUP BY curso
ORDER BY curso;

-- =====================================================
-- 4. ALUMNOS SIN CALIFICACIONES
-- =====================================================
SELECT '=== ALUMNOS SIN CALIFICACIONES ===' AS info;

SELECT 
    a.id,
    CONCAT(a.apellido, ', ', a.nombre) as alumno,
    CONCAT(a.curso, ' - ', a.division) as curso_division,
    'Sin calificaciones registradas' as estado
FROM alumnos a
LEFT JOIN calificaciones c ON a.id = c.alumno_id
WHERE a.activo = TRUE AND c.id IS NULL
ORDER BY a.curso, a.division, a.apellido;

-- =====================================================
-- 5. ALUMNOS CON CALIFICACIONES
-- =====================================================
SELECT '=== ALUMNOS CON CALIFICACIONES ===' AS info;

SELECT 
    a.id,
    CONCAT(a.apellido, ', ', a.nombre) as alumno,
    CONCAT(a.curso, ' - ', a.division) as curso_division,
    COUNT(c.id) as total_calificaciones,
    ROUND(AVG(c.nota), 2) as promedio_general
FROM alumnos a
INNER JOIN calificaciones c ON a.id = c.alumno_id
WHERE a.activo = TRUE
GROUP BY a.id, a.nombre, a.apellido, a.curso, a.division
ORDER BY promedio_general DESC;

-- =====================================================
-- 6. BUSCAR ALUMNO POR NOMBRE
-- =====================================================
-- Cambiar 'NOMBRE_A_BUSCAR' por el nombre que quieras buscar
/*
SELECT '=== BUSCAR ALUMNO ===' AS info;

SELECT 
    id,
    CONCAT(apellido, ', ', nombre) as alumno,
    dni,
    CONCAT(curso, ' - ', division) as curso_division,
    DATE_FORMAT(fecha_nacimiento, '%d/%m/%Y') as fecha_nacimiento
FROM alumnos 
WHERE activo = TRUE 
AND (nombre LIKE '%NOMBRE_A_BUSCAR%' OR apellido LIKE '%NOMBRE_A_BUSCAR%')
ORDER BY apellido, nombre;
*/

-- =====================================================
-- 7. ALUMNOS POR PADRE
-- =====================================================
SELECT '=== ALUMNOS POR PADRE ===' AS info;

SELECT 
    u.nombre_usuario as padre,
    COUNT(a.id) as total_hijos,
    GROUP_CONCAT(
        CONCAT(a.apellido, ', ', a.nombre, ' (', a.curso, ' ', a.division, ')')
        ORDER BY a.curso, a.apellido 
        SEPARATOR ' | '
    ) as hijos
FROM usuarios u
LEFT JOIN alumnos a ON u.id = a.padre_id AND a.activo = TRUE
WHERE u.tipo_usuario = 'Padre'
GROUP BY u.id, u.nombre_usuario
ORDER BY u.nombre_usuario;

-- =====================================================
-- 8. RESUMEN GENERAL
-- =====================================================
SELECT '=== RESUMEN GENERAL ===' AS info;

SELECT 
    'Total de alumnos activos' as descripcion,
    COUNT(*) as cantidad
FROM alumnos 
WHERE activo = TRUE

UNION ALL

SELECT 
    'Alumnos con calificaciones' as descripcion,
    COUNT(DISTINCT alumno_id) as cantidad
FROM calificaciones

UNION ALL

SELECT 
    'Alumnos sin calificaciones' as descripcion,
    COUNT(*) as cantidad
FROM alumnos a
LEFT JOIN calificaciones c ON a.id = c.alumno_id
WHERE a.activo = TRUE AND c.id IS NULL

UNION ALL

SELECT 
    'Promedio general de edad' as descripcion,
    ROUND(AVG(TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE())), 1) as cantidad
FROM alumnos 
WHERE activo = TRUE;