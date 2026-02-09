"""
Operaciones de Reportes para el Sistema de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
from ..database import crear_conexion

class ReportesOperations:
    """Operaciones especializadas para generación de reportes"""
    
    def __init__(self):
        self.connection = None
    
    def conectar(self):
        """Establecer conexión a la base de datos"""
        self.connection = crear_conexion()
        return self.connection is not None
    
    def desconectar(self):
        """Cerrar conexión a la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def obtener_datos_reporte_curso(self, curso: str, division: str, periodo_id: int) -> Dict:
        """Obtener datos completos para reporte de curso"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            
            # Información general del curso
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT a.id) as total_alumnos,
                    COUNT(DISTINCT m.id) as total_materias,
                    ROUND(AVG(c.nota), 2) as promedio_curso,
                    COUNT(c.id) as total_calificaciones,
                    COUNT(CASE WHEN c.nota >= 6.0 THEN 1 END) as aprobados,
                    COUNT(CASE WHEN c.nota < 6.0 THEN 1 END) as desaprobados
                FROM alumnos a
                JOIN calificaciones c ON a.id = c.alumno_id
                JOIN materias m ON c.materia_id = m.id
                WHERE a.curso = %s AND a.division = %s AND c.periodo_id = %s
            """, (curso, division, periodo_id))
            
            info_general = cursor.fetchone()
            
            # Promedios por materia
            cursor.execute("""
                SELECT 
                    m.nombre as materia,
                    ROUND(AVG(c.nota), 2) as promedio_materia,
                    COUNT(c.nota) as evaluaciones,
                    COUNT(CASE WHEN c.nota >= 6.0 THEN 1 END) as aprobados,
                    COUNT(CASE WHEN c.nota < 6.0 THEN 1 END) as desaprobados
                FROM calificaciones c
                JOIN materias m ON c.materia_id = m.id
                JOIN alumnos a ON c.alumno_id = a.id
                WHERE a.curso = %s AND a.division = %s AND c.periodo_id = %s
                GROUP BY m.id, m.nombre
                ORDER BY promedio_materia DESC
            """, (curso, division, periodo_id))
            
            promedios_materias = cursor.fetchall()
            
            cursor.close()
            
            return {
                'info_general': info_general,
                'promedios_materias': promedios_materias
            }
            
        except Error as e:
            print(f"Error al obtener datos de reporte: {e}")
            return {}
        finally:
            self.desconectar()
    
    def obtener_datos_reporte_alumno(self, alumno_id: int, periodo_id: int) -> Dict:
        """Obtener datos completos para reporte individual de alumno"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            
            # Información del alumno
            cursor.execute("""
                SELECT 
                    CONCAT(a.apellido, ', ', a.nombre) as alumno,
                    a.curso, a.division, a.dni,
                    u.nombre_usuario as padre
                FROM alumnos a
                LEFT JOIN usuarios u ON a.padre_id = u.id
                WHERE a.id = %s
            """, (alumno_id,))
            
            info_alumno = cursor.fetchone()
            
            # Calificaciones por materia
            cursor.execute("""
                SELECT 
                    m.nombre as materia,
                    ROUND(AVG(c.nota), 2) as promedio,
                    COUNT(c.nota) as evaluaciones,
                    MIN(c.nota) as nota_minima,
                    MAX(c.nota) as nota_maxima
                FROM calificaciones c
                JOIN materias m ON c.materia_id = m.id
                WHERE c.alumno_id = %s AND c.periodo_id = %s
                GROUP BY m.id, m.nombre
                ORDER BY m.nombre
            """, (alumno_id, periodo_id))
            
            calificaciones_materias = cursor.fetchall()
            
            cursor.close()
            
            return {
                'info_alumno': info_alumno,
                'calificaciones_materias': calificaciones_materias
            }
            
        except Error as e:
            print(f"Error al obtener datos de reporte de alumno: {e}")
            return {}
        finally:
            self.desconectar()
    
    def obtener_datos_comparativo_temporal(self, curso: str = None, materia_id: int = None) -> List[Dict]:
        """Obtener datos para análisis comparativo temporal"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if curso and materia_id:
                query = """
                    SELECT 
                        p.nombre as periodo,
                        ROUND(AVG(c.nota), 2) as promedio,
                        COUNT(DISTINCT a.id) as alumnos,
                        COUNT(c.nota) as evaluaciones
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    WHERE a.curso = %s AND c.materia_id = %s
                    GROUP BY p.id, p.nombre
                    ORDER BY p.fecha_inicio
                """
                cursor.execute(query, (curso, materia_id))
            elif curso:
                query = """
                    SELECT 
                        p.nombre as periodo,
                        ROUND(AVG(c.nota), 2) as promedio,
                        COUNT(DISTINCT a.id) as alumnos,
                        COUNT(c.nota) as evaluaciones
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    WHERE a.curso = %s
                    GROUP BY p.id, p.nombre
                    ORDER BY p.fecha_inicio
                """
                cursor.execute(query, (curso,))
            else:
                query = """
                    SELECT 
                        p.nombre as periodo,
                        ROUND(AVG(c.nota), 2) as promedio,
                        COUNT(DISTINCT a.id) as alumnos,
                        COUNT(c.nota) as evaluaciones
                    FROM calificaciones c
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    GROUP BY p.id, p.nombre
                    ORDER BY p.fecha_inicio
                """
                cursor.execute(query)
            
            datos_temporales = cursor.fetchall()
            cursor.close()
            return datos_temporales
            
        except Error as e:
            print(f"Error al obtener datos comparativos temporales: {e}")
            return []
        finally:
            self.desconectar()