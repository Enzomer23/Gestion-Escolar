"""
Operaciones de base de datos para el módulo de evaluaciones institucionales
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Optional
from .database import crear_conexion

class EvaluacionesManager:
    """Gestor de operaciones de evaluaciones institucionales"""
    
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
    
    def crear_encuesta(self, titulo: str, descripcion: str, tipo_encuesta: str,
                      dirigida_a: str, creador_id: int, fecha_cierre: date) -> bool:
        """Crear una nueva encuesta"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            query = """
                INSERT INTO encuestas_institucionales 
                (titulo, descripcion, tipo_encuesta, dirigida_a, creador_id, 
                 fecha_cierre, estado)
                VALUES (%s, %s, %s, %s, %s, %s, 'Activa')
            """
            cursor.execute(query, (titulo, descripcion, tipo_encuesta, dirigida_a, 
                                 creador_id, fecha_cierre))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            print(f"Error al crear encuesta: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_encuestas_activas(self, dirigida_a: str = None) -> List[Dict]:
        """Obtener encuestas activas"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if dirigida_a:
                query = """
                    SELECT 
                        e.id,
                        e.titulo,
                        e.descripcion,
                        e.tipo_encuesta,
                        e.fecha_creacion,
                        e.fecha_cierre,
                        u.nombre_usuario as creador,
                        COUNT(r.id) as total_respuestas
                    FROM encuestas_institucionales e
                    JOIN usuarios u ON e.creador_id = u.id
                    LEFT JOIN respuestas_encuestas r ON e.id = r.encuesta_id
                    WHERE e.estado = 'Activa' 
                    AND (e.dirigida_a = %s OR e.dirigida_a = 'Toda la comunidad')
                    AND e.fecha_cierre >= CURDATE()
                    GROUP BY e.id
                    ORDER BY e.fecha_cierre
                """
                cursor.execute(query, (dirigida_a,))
            else:
                query = """
                    SELECT 
                        e.id,
                        e.titulo,
                        e.descripcion,
                        e.tipo_encuesta,
                        e.dirigida_a,
                        e.fecha_creacion,
                        e.fecha_cierre,
                        u.nombre_usuario as creador,
                        COUNT(r.id) as total_respuestas
                    FROM encuestas_institucionales e
                    JOIN usuarios u ON e.creador_id = u.id
                    LEFT JOIN respuestas_encuestas r ON e.id = r.encuesta_id
                    WHERE e.estado = 'Activa' AND e.fecha_cierre >= CURDATE()
                    GROUP BY e.id
                    ORDER BY e.fecha_cierre
                """
                cursor.execute(query)
            
            encuestas = cursor.fetchall()
            cursor.close()
            return encuestas
            
        except Exception as e:
            print(f"Error al obtener encuestas activas: {e}")
            return []
        finally:
            self.desconectar()
    
    def responder_encuesta(self, encuesta_id: int, usuario_id: int, 
                          respuestas: List[Dict]) -> bool:
        """Registrar respuesta a una encuesta"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            
            for respuesta in respuestas:
                query = """
                    INSERT INTO respuestas_encuestas 
                    (encuesta_id, usuario_id, pregunta, respuesta, puntuacion)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    encuesta_id,
                    usuario_id,
                    respuesta['pregunta'],
                    respuesta['respuesta'],
                    respuesta.get('puntuacion', None)
                ))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            print(f"Error al responder encuesta: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_resultados_encuesta(self, encuesta_id: int) -> Dict:
        """Obtener resultados de una encuesta"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            
            # Información básica de la encuesta
            cursor.execute("""
                SELECT titulo, descripcion, tipo_encuesta, dirigida_a
                FROM encuestas_institucionales 
                WHERE id = %s
            """, (encuesta_id,))
            info_encuesta = cursor.fetchone()
            
            # Estadísticas de respuestas
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT usuario_id) as total_participantes,
                    AVG(puntuacion) as promedio_satisfaccion,
                    COUNT(*) as total_respuestas
                FROM respuestas_encuestas 
                WHERE encuesta_id = %s
            """, (encuesta_id,))
            estadisticas = cursor.fetchone()
            
            cursor.close()
            
            return {
                'info': info_encuesta,
                'estadisticas': estadisticas
            }
            
        except Exception as e:
            print(f"Error al obtener resultados de encuesta: {e}")
            return {}
        finally:
            self.desconectar()