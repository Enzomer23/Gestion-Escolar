"""
Operaciones de Estadísticas para el Sistema de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
from ..database import crear_conexion

class EstadisticasOperations:
    """Operaciones especializadas para estadísticas académicas"""
    
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
    
    def obtener_estadisticas_curso(self, curso: str, division: str, periodo_id: int) -> Dict:
        """Obtener estadísticas generales de un curso"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    COUNT(DISTINCT a.id) as total_alumnos,
                    COUNT(DISTINCT m.id) as total_materias,
                    ROUND(AVG(c.nota), 2) as promedio_curso,
                    COUNT(c.id) as total_calificaciones
                FROM alumnos a
                JOIN calificaciones c ON a.id = c.alumno_id
                JOIN materias m ON c.materia_id = m.id
                WHERE a.curso = %s AND a.division = %s AND c.periodo_id = %s
            """
            cursor.execute(query, (curso, division, periodo_id))
            estadisticas = cursor.fetchone()
            cursor.close()
            
            return estadisticas or {}
            
        except Error as e:
            print(f"Error al obtener estadísticas del curso: {e}")
            return {}
        finally:
            self.desconectar()
    
    def obtener_alumnos_en_riesgo(self, periodo_id: int, promedio_minimo: float = 6.0) -> List[Dict]:
        """Obtener alumnos con promedio por debajo del mínimo"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    a.id,
                    CONCAT(a.apellido, ', ', a.nombre) as alumno,
                    a.curso, a.division,
                    ROUND(AVG(pa.promedio), 2) as promedio_general,
                    COUNT(pa.materia_id) as materias_cursadas
                FROM alumnos a
                JOIN promedios_alumnos pa ON a.id = pa.alumno_id
                WHERE pa.periodo_id = %s AND a.activo = TRUE
                GROUP BY a.id
                HAVING promedio_general < %s
                ORDER BY promedio_general ASC
            """
            cursor.execute(query, (periodo_id, promedio_minimo))
            alumnos_riesgo = cursor.fetchall()
            cursor.close()
            return alumnos_riesgo
            
        except Error as e:
            print(f"Error al obtener alumnos en riesgo: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_ranking_alumnos(self, materia_id: int, periodo_id: int) -> List[Dict]:
        """Obtener ranking de alumnos ordenados por promedio"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    a.id AS alumno_id,
                    CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                    a.curso, a.division,
                    ROUND(AVG(c.nota), 2) AS promedio,
                    COUNT(c.nota) AS cantidad_notas,
                    MIN(c.nota) AS nota_minima,
                    MAX(c.nota) AS nota_maxima,
                    CASE 
                        WHEN AVG(c.nota) >= 9.0 THEN 'Excelente'
                        WHEN AVG(c.nota) >= 8.0 THEN 'Muy Bueno'
                        WHEN AVG(c.nota) >= 7.0 THEN 'Bueno'
                        WHEN AVG(c.nota) >= 6.0 THEN 'Regular'
                        ELSE 'En Riesgo'
                    END AS categoria
                FROM calificaciones c
                JOIN alumnos a ON c.alumno_id = a.id
                WHERE c.materia_id = %s AND c.periodo_id = %s AND a.activo = TRUE
                GROUP BY a.id
                ORDER BY promedio DESC, a.apellido, a.nombre
            """
            cursor.execute(query, (materia_id, periodo_id))
            ranking = cursor.fetchall()
            cursor.close()
            return ranking
            
        except Error as e:
            print(f"Error al obtener ranking de alumnos: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_tendencias_promedios(self, materia_id: int, alumno_id: int = None) -> List[Dict]:
        """Obtener tendencias de promedios a lo largo del tiempo"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if alumno_id:
                query = """
                    SELECT 
                        p.nombre AS periodo,
                        ROUND(AVG(c.nota), 2) AS promedio,
                        COUNT(c.nota) AS cantidad_notas,
                        DATE_FORMAT(MIN(c.fecha_evaluacion), '%m/%Y') AS mes_año
                    FROM calificaciones c
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    WHERE c.materia_id = %s AND c.alumno_id = %s
                    GROUP BY p.id
                    ORDER BY p.fecha_inicio
                """
                cursor.execute(query, (materia_id, alumno_id))
            else:
                query = """
                    SELECT 
                        p.nombre AS periodo,
                        ROUND(AVG(c.nota), 2) AS promedio,
                        COUNT(DISTINCT c.alumno_id) AS alumnos_evaluados,
                        COUNT(c.nota) AS total_evaluaciones
                    FROM calificaciones c
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    WHERE c.materia_id = %s
                    GROUP BY p.id
                    ORDER BY p.fecha_inicio
                """
                cursor.execute(query, (materia_id,))
            
            tendencias = cursor.fetchall()
            cursor.close()
            return tendencias
            
        except Error as e:
            print(f"Error al obtener tendencias de promedios: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_estadisticas_promedios_curso(self, curso: str, division: str, periodo_id: int) -> Dict:
        """Obtener estadísticas detalladas de promedios de un curso"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    COUNT(DISTINCT a.id) as total_alumnos,
                    ROUND(AVG(c.nota), 2) as promedio_general,
                    ROUND(STDDEV(c.nota), 2) as desviacion_estandar,
                    MIN(c.nota) as nota_minima,
                    MAX(c.nota) as nota_maxima,
                    COUNT(c.id) as total_evaluaciones,
                    COUNT(CASE WHEN c.nota >= 9.0 THEN 1 END) as notas_excelentes,
                    COUNT(CASE WHEN c.nota >= 8.0 AND c.nota < 9.0 THEN 1 END) as notas_muy_buenas,
                    COUNT(CASE WHEN c.nota >= 7.0 AND c.nota < 8.0 THEN 1 END) as notas_buenas,
                    COUNT(CASE WHEN c.nota >= 6.0 AND c.nota < 7.0 THEN 1 END) as notas_regulares,
                    COUNT(CASE WHEN c.nota < 6.0 THEN 1 END) as notas_en_riesgo
                FROM alumnos a
                JOIN calificaciones c ON a.id = c.alumno_id
                WHERE a.curso = %s AND a.division = %s AND c.periodo_id = %s AND a.activo = TRUE
            """
            cursor.execute(query, (curso, division, periodo_id))
            estadisticas = cursor.fetchone()
            cursor.close()
            
            return estadisticas or {}
            
        except Error as e:
            print(f"Error al obtener estadísticas de promedios: {e}")
            return {}
        finally:
            self.desconectar()