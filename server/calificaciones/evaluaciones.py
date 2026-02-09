"""
Operaciones de Evaluaciones para el Sistema de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Optional
from ..database import crear_conexion

class EvaluacionesOperations:
    """Operaciones especializadas para gestión de evaluaciones"""
    
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
    
    def obtener_periodos_activos(self) -> List[Dict]:
        """Obtener períodos de evaluación activos"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, ano_lectivo
                FROM periodos_evaluacion 
                WHERE activo = TRUE
                ORDER BY fecha_inicio
            """
            cursor.execute(query)
            periodos = cursor.fetchall()
            cursor.close()
            return periodos
            
        except Error as e:
            print(f"Error al obtener períodos: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_tipos_evaluacion(self) -> List[Dict]:
        """Obtener tipos de evaluación disponibles"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, nombre, descripcion, peso_porcentual
                FROM tipos_evaluacion 
                WHERE activo = TRUE
                ORDER BY nombre
            """
            cursor.execute(query)
            tipos = cursor.fetchall()
            cursor.close()
            return tipos
            
        except Error as e:
            print(f"Error al obtener tipos de evaluación: {e}")
            return []
        finally:
            self.desconectar()
    
    def registrar_calificacion(self, alumno_id: int, materia_id: int, docente_id: int, 
                             periodo_id: int, tipo_evaluacion_id: int, nota: float, 
                             fecha_evaluacion: date, observaciones: str = "") -> bool:
        """Registrar una nueva calificación"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            query = """
                INSERT INTO calificaciones 
                (alumno_id, materia_id, docente_id, periodo_id, tipo_evaluacion_id, 
                 nota, fecha_evaluacion, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                nota = VALUES(nota),
                observaciones = VALUES(observaciones),
                fecha_modificacion = CURRENT_TIMESTAMP
            """
            cursor.execute(query, (alumno_id, materia_id, docente_id, periodo_id, 
                                 tipo_evaluacion_id, nota, fecha_evaluacion, observaciones))
            
            self.connection.commit()
            cursor.close()
            
            # Actualizar promedios automáticamente
            from .promedios import PromediosOperations
            promedios_ops = PromediosOperations()
            promedios_ops.actualizar_simple(alumno_id, materia_id, periodo_id)
            
            return True
            
        except Error as e:
            print(f"Error al registrar calificación: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_calificaciones_alumno(self, alumno_id: int, periodo_id: int = None) -> List[Dict]:
        """Obtener calificaciones de un alumno específico"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if periodo_id:
                query = """
                    SELECT 
                        c.id, c.alumno_id, c.materia_id, c.periodo_id, c.tipo_evaluacion_id,
                        CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                        a.curso, a.division,
                        m.nombre AS materia, m.codigo AS codigo_materia,
                        u.nombre_usuario AS docente,
                        p.nombre AS periodo,
                        te.nombre AS tipo_evaluacion,
                        c.nota, c.fecha_evaluacion, c.observaciones, c.fecha_registro
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN materias m ON c.materia_id = m.id
                    JOIN usuarios u ON c.docente_id = u.id
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    JOIN tipos_evaluacion te ON c.tipo_evaluacion_id = te.id
                    WHERE c.alumno_id = %s AND c.periodo_id = %s 
                    AND a.activo = TRUE AND m.activa = TRUE
                    ORDER BY m.nombre, c.fecha_evaluacion
                """
                cursor.execute(query, (alumno_id, periodo_id))
            else:
                query = """
                    SELECT 
                        c.id, c.alumno_id, c.materia_id, c.periodo_id, c.tipo_evaluacion_id,
                        CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                        a.curso, a.division,
                        m.nombre AS materia, m.codigo AS codigo_materia,
                        u.nombre_usuario AS docente,
                        p.nombre AS periodo,
                        te.nombre AS tipo_evaluacion,
                        c.nota, c.fecha_evaluacion, c.observaciones, c.fecha_registro
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN materias m ON c.materia_id = m.id
                    JOIN usuarios u ON c.docente_id = u.id
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    JOIN tipos_evaluacion te ON c.tipo_evaluacion_id = te.id
                    WHERE c.alumno_id = %s AND a.activo = TRUE AND m.activa = TRUE
                    ORDER BY p.nombre, m.nombre, c.fecha_evaluacion
                """
                cursor.execute(query, (alumno_id,))
            
            calificaciones = cursor.fetchall()
            cursor.close()
            return calificaciones
            
        except Error as e:
            print(f"Error al obtener calificaciones del alumno: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_calificaciones_materia(self, materia_id: int, periodo_id: int) -> List[Dict]:
        """Obtener todas las calificaciones de una materia en un período"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    c.id, c.alumno_id, c.materia_id, c.periodo_id, c.tipo_evaluacion_id,
                    CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                    a.curso, a.division,
                    m.nombre AS materia, m.codigo AS codigo_materia,
                    u.nombre_usuario AS docente,
                    p.nombre AS periodo,
                    te.nombre AS tipo_evaluacion,
                    c.nota, c.fecha_evaluacion, c.observaciones, c.fecha_registro
                FROM calificaciones c
                JOIN alumnos a ON c.alumno_id = a.id
                JOIN materias m ON c.materia_id = m.id
                JOIN usuarios u ON c.docente_id = u.id
                JOIN periodos_evaluacion p ON c.periodo_id = p.id
                JOIN tipos_evaluacion te ON c.tipo_evaluacion_id = te.id
                WHERE c.materia_id = %s AND c.periodo_id = %s 
                AND a.activo = TRUE AND m.activa = TRUE
                ORDER BY a.apellido, a.nombre, te.nombre, c.fecha_evaluacion
            """
            cursor.execute(query, (materia_id, periodo_id))
            calificaciones = cursor.fetchall()
            cursor.close()
            return calificaciones
            
        except Error as e:
            print(f"Error al obtener calificaciones de la materia: {e}")
            return []
        finally:
            self.desconectar()