"""
Operaciones de Alumnos para el Sistema de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
from ..database import crear_conexion

class AlumnosOperations:
    """Operaciones especializadas para gestión de alumnos"""
    
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
    
    def obtener_por_curso(self, curso: str, division: str = 'A') -> List[Dict]:
        """Obtener lista de alumnos por curso y división"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, nombre, apellido, dni, curso, division, fecha_nacimiento
                FROM alumnos 
                WHERE curso = %s AND division = %s AND activo = TRUE
                ORDER BY apellido, nombre
            """
            cursor.execute(query, (curso, division))
            alumnos = cursor.fetchall()
            cursor.close()
            return alumnos
            
        except Error as e:
            print(f"Error al obtener alumnos: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_por_id(self, alumno_id: int) -> Optional[Dict]:
        """Obtener información de un alumno específico"""
        try:
            if not self.conectar():
                return None
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT a.*, CONCAT(u.nombre_usuario) as padre_nombre
                FROM alumnos a
                LEFT JOIN usuarios u ON a.padre_id = u.id
                WHERE a.id = %s AND a.activo = TRUE
            """
            cursor.execute(query, (alumno_id,))
            alumno = cursor.fetchone()
            cursor.close()
            return alumno
            
        except Error as e:
            print(f"Error al obtener alumno: {e}")
            return None
        finally:
            self.desconectar()
    
    def buscar_por_nombre(self, nombre: str) -> List[Dict]:
        """Buscar alumnos por nombre o apellido"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, nombre, apellido, dni, curso, division
                FROM alumnos 
                WHERE (nombre LIKE %s OR apellido LIKE %s) AND activo = TRUE
                ORDER BY apellido, nombre
            """
            patron = f"%{nombre}%"
            cursor.execute(query, (patron, patron))
            alumnos = cursor.fetchall()
            cursor.close()
            return alumnos
            
        except Error as e:
            print(f"Error al buscar alumnos: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_todos_activos(self) -> List[Dict]:
        """Obtener todos los alumnos activos"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, nombre, apellido, dni, curso, division, fecha_nacimiento
                FROM alumnos 
                WHERE activo = TRUE
                ORDER BY curso, division, apellido, nombre
            """
            cursor.execute(query)
            alumnos = cursor.fetchall()
            cursor.close()
            return alumnos
            
        except Error as e:
            print(f"Error al obtener todos los alumnos: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_estadisticas_generales(self) -> Dict:
        """Obtener estadísticas generales de alumnos"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    COUNT(*) as total_alumnos,
                    COUNT(CASE WHEN curso = '1º Año' THEN 1 END) as primer_año,
                    COUNT(CASE WHEN curso = '2º Año' THEN 1 END) as segundo_año,
                    COUNT(CASE WHEN curso = '3º Año' THEN 1 END) as tercer_año,
                    ROUND(AVG(TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE())), 1) as edad_promedio
                FROM alumnos 
                WHERE activo = TRUE
            """
            cursor.execute(query)
            estadisticas = cursor.fetchone()
            cursor.close()
            return estadisticas or {}
            
        except Error as e:
            print(f"Error al obtener estadísticas de alumnos: {e}")
            return {}
        finally:
            self.desconectar()