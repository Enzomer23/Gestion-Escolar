"""
Operaciones de Materias para el Sistema de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
from ..database import crear_conexion

class MateriasOperations:
    """Operaciones especializadas para gestión de materias"""
    
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
    
    def obtener_por_docente(self, docente_id: int) -> List[Dict]:
        """Obtener materias asignadas a un docente"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, nombre, codigo, curso, division, horas_semanales
                FROM materias 
                WHERE docente_id = %s AND activa = TRUE
                ORDER BY curso, nombre
            """
            cursor.execute(query, (docente_id,))
            materias = cursor.fetchall()
            cursor.close()
            return materias
            
        except Error as e:
            print(f"Error al obtener materias: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_por_curso(self, curso: str, division: str = 'A') -> List[Dict]:
        """Obtener materias de un curso específico"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT m.*, CONCAT(u.nombre_usuario) as docente_nombre
                FROM materias m
                LEFT JOIN usuarios u ON m.docente_id = u.id
                WHERE m.curso = %s AND m.division = %s AND m.activa = TRUE
                ORDER BY m.nombre
            """
            cursor.execute(query, (curso, division))
            materias = cursor.fetchall()
            cursor.close()
            return materias
            
        except Error as e:
            print(f"Error al obtener materias por curso: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_por_id(self, materia_id: int) -> Optional[Dict]:
        """Obtener información de una materia específica"""
        try:
            if not self.conectar():
                return None
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT m.*, u.nombre_usuario as docente_nombre
                FROM materias m
                LEFT JOIN usuarios u ON m.docente_id = u.id
                WHERE m.id = %s AND m.activa = TRUE
            """
            cursor.execute(query, (materia_id,))
            materia = cursor.fetchone()
            cursor.close()
            return materia
            
        except Error as e:
            print(f"Error al obtener materia: {e}")
            return None
        finally:
            self.desconectar()
    
    def obtener_estadisticas_materia(self, materia_id: int, periodo_id: int) -> Dict:
        """Obtener estadísticas de una materia específica"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    COUNT(DISTINCT c.alumno_id) as alumnos_evaluados,
                    COUNT(c.id) as total_evaluaciones,
                    ROUND(AVG(c.nota), 2) as promedio_materia,
                    ROUND(STDDEV(c.nota), 2) as desviacion_estandar,
                    MIN(c.nota) as nota_minima,
                    MAX(c.nota) as nota_maxima,
                    COUNT(CASE WHEN c.nota >= 6.0 THEN 1 END) as aprobados,
                    COUNT(CASE WHEN c.nota < 6.0 THEN 1 END) as desaprobados
                FROM calificaciones c
                WHERE c.materia_id = %s AND c.periodo_id = %s
            """
            cursor.execute(query, (materia_id, periodo_id))
            estadisticas = cursor.fetchone()
            cursor.close()
            return estadisticas or {}
            
        except Error as e:
            print(f"Error al obtener estadísticas de materia: {e}")
            return {}
        finally:
            self.desconectar()
    
    def obtener_todas_activas(self) -> List[Dict]:
        """Obtener todas las materias activas"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT m.*, u.nombre_usuario as docente_nombre
                FROM materias m
                LEFT JOIN usuarios u ON m.docente_id = u.id
                WHERE m.activa = TRUE
                ORDER BY m.curso, m.division, m.nombre
            """
            cursor.execute(query)
            materias = cursor.fetchall()
            cursor.close()
            return materias
            
        except Error as e:
            print(f"Error al obtener todas las materias: {e}")
            return []
        finally:
            self.desconectar()