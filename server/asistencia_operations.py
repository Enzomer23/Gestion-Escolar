"""
Operaciones de base de datos para el módulo de asistencia
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from .database import crear_conexion

class AsistenciaManager:
    """Gestor de operaciones de asistencia en la base de datos"""
    
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
    
    def registrar_asistencia_diaria(self, fecha: date, curso: str, division: str, 
                                   asistencias: List[Dict]) -> bool:
        """
        Registrar asistencia diaria de un curso
        
        Args:
            fecha: Fecha de la asistencia
            curso: Curso (ej: "1º Año")
            division: División (ej: "A")
            asistencias: Lista de dict con alumno_id y estado
        
        Returns:
            bool: True si se registró correctamente
        """
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            
            for asistencia in asistencias:
                query = """
                    INSERT INTO asistencia_diaria 
                    (alumno_id, fecha, estado, observaciones, registrado_por)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    estado = VALUES(estado),
                    observaciones = VALUES(observaciones),
                    fecha_modificacion = CURRENT_TIMESTAMP
                """
                cursor.execute(query, (
                    asistencia['alumno_id'],
                    fecha,
                    asistencia['estado'],
                    asistencia.get('observaciones', ''),
                    asistencia.get('registrado_por', 1)  # ID del docente/preceptor
                ))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            print(f"Error al registrar asistencia: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_asistencia_alumno(self, alumno_id: int, fecha_inicio: date = None, 
                                 fecha_fin: date = None) -> List[Dict]:
        """Obtener historial de asistencia de un alumno"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if fecha_inicio and fecha_fin:
                query = """
                    SELECT 
                        ad.fecha,
                        ad.estado,
                        ad.observaciones,
                        CONCAT(a.apellido, ', ', a.nombre) as alumno,
                        a.curso,
                        a.division
                    FROM asistencia_diaria ad
                    JOIN alumnos a ON ad.alumno_id = a.id
                    WHERE ad.alumno_id = %s AND ad.fecha BETWEEN %s AND %s
                    ORDER BY ad.fecha DESC
                """
                cursor.execute(query, (alumno_id, fecha_inicio, fecha_fin))
            else:
                query = """
                    SELECT 
                        ad.fecha,
                        ad.estado,
                        ad.observaciones,
                        CONCAT(a.apellido, ', ', a.nombre) as alumno,
                        a.curso,
                        a.division
                    FROM asistencia_diaria ad
                    JOIN alumnos a ON ad.alumno_id = a.id
                    WHERE ad.alumno_id = %s
                    ORDER BY ad.fecha DESC
                    LIMIT 30
                """
                cursor.execute(query, (alumno_id,))
            
            asistencias = cursor.fetchall()
            cursor.close()
            return asistencias
            
        except Error as e:
            print(f"Error al obtener asistencia del alumno: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_estadisticas_asistencia_curso(self, curso: str, division: str, 
                                            fecha_inicio: date, fecha_fin: date) -> Dict:
        """Obtener estadísticas de asistencia de un curso"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    COUNT(DISTINCT ad.alumno_id) as total_alumnos,
                    COUNT(CASE WHEN ad.estado = 'Presente' THEN 1 END) as total_presentes,
                    COUNT(CASE WHEN ad.estado = 'Ausente' THEN 1 END) as total_ausentes,
                    COUNT(CASE WHEN ad.estado = 'Tarde' THEN 1 END) as total_tardes,
                    ROUND(
                        (COUNT(CASE WHEN ad.estado = 'Presente' THEN 1 END) * 100.0) / 
                        COUNT(*), 2
                    ) as porcentaje_asistencia
                FROM asistencia_diaria ad
                JOIN alumnos a ON ad.alumno_id = a.id
                WHERE a.curso = %s AND a.division = %s 
                AND ad.fecha BETWEEN %s AND %s
            """
            cursor.execute(query, (curso, division, fecha_inicio, fecha_fin))
            estadisticas = cursor.fetchone()
            cursor.close()
            
            return estadisticas or {}
            
        except Error as e:
            print(f"Error al obtener estadísticas de asistencia: {e}")
            return {}
        finally:
            self.desconectar()
    
    def obtener_alumnos_inasistencias_reiteradas(self, dias_limite: int = 5) -> List[Dict]:
        """Obtener alumnos con inasistencias reiteradas"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    a.id,
                    CONCAT(a.apellido, ', ', a.nombre) as alumno,
                    a.curso,
                    a.division,
                    COUNT(CASE WHEN ad.estado = 'Ausente' THEN 1 END) as total_ausencias,
                    COUNT(*) as dias_registrados,
                    ROUND(
                        (COUNT(CASE WHEN ad.estado = 'Presente' THEN 1 END) * 100.0) / 
                        COUNT(*), 2
                    ) as porcentaje_asistencia
                FROM alumnos a
                JOIN asistencia_diaria ad ON a.id = ad.alumno_id
                WHERE a.activo = TRUE 
                AND ad.fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY a.id
                HAVING total_ausencias >= %s
                ORDER BY total_ausencias DESC
            """
            cursor.execute(query, (dias_limite,))
            alumnos = cursor.fetchall()
            cursor.close()
            return alumnos
            
        except Error as e:
            print(f"Error al obtener alumnos con inasistencias reiteradas: {e}")
            return []
        finally:
            self.desconectar()