"""
Operaciones de base de datos para el módulo de eventos
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Optional
from .database import crear_conexion

class EventosManager:
    """Gestor de operaciones de eventos en la base de datos"""
    
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
    
    def crear_evento(self, titulo: str, descripcion: str, fecha_evento: date,
                    hora_inicio: str, hora_fin: str, tipo_evento: str,
                    organizador_id: int, dirigido_a: str = "Toda la comunidad") -> bool:
        """Crear un nuevo evento"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            query = """
                INSERT INTO eventos_institucionales 
                (titulo, descripcion, fecha_evento, hora_inicio, hora_fin, 
                 tipo_evento, organizador_id, dirigido_a, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Programado')
            """
            cursor.execute(query, (titulo, descripcion, fecha_evento, hora_inicio, 
                                 hora_fin, tipo_evento, organizador_id, dirigido_a))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            print(f"Error al crear evento: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_eventos_proximos(self, dias_adelante: int = 30) -> List[Dict]:
        """Obtener eventos próximos"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    e.id,
                    e.titulo,
                    e.descripcion,
                    e.fecha_evento,
                    e.hora_inicio,
                    e.hora_fin,
                    e.tipo_evento,
                    e.dirigido_a,
                    e.estado,
                    u.nombre_usuario as organizador,
                    DATEDIFF(e.fecha_evento, CURDATE()) as dias_restantes
                FROM eventos_institucionales e
                JOIN usuarios u ON e.organizador_id = u.id
                WHERE e.fecha_evento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
                AND e.estado IN ('Programado', 'Confirmado')
                ORDER BY e.fecha_evento, e.hora_inicio
            """
            cursor.execute(query, (dias_adelante,))
            eventos = cursor.fetchall()
            cursor.close()
            return eventos
            
        except Exception as e:
            print(f"Error al obtener eventos próximos: {e}")
            return []
        finally:
            self.desconectar()
    
    def registrar_participacion(self, evento_id: int, participante_id: int, 
                              tipo_participante: str, confirmado: bool = False) -> bool:
        """Registrar participación en un evento"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            query = """
                INSERT INTO participacion_eventos 
                (evento_id, participante_id, tipo_participante, confirmado, fecha_registro)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON DUPLICATE KEY UPDATE
                confirmado = VALUES(confirmado)
            """
            cursor.execute(query, (evento_id, participante_id, tipo_participante, confirmado))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            print(f"Error al registrar participación: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_calendario_mensual(self, año: int, mes: int) -> List[Dict]:
        """Obtener eventos del calendario mensual"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    e.id,
                    e.titulo,
                    e.fecha_evento,
                    e.hora_inicio,
                    e.tipo_evento,
                    e.estado,
                    COUNT(pe.participante_id) as total_participantes
                FROM eventos_institucionales e
                LEFT JOIN participacion_eventos pe ON e.id = pe.evento_id
                WHERE YEAR(e.fecha_evento) = %s AND MONTH(e.fecha_evento) = %s
                GROUP BY e.id
                ORDER BY e.fecha_evento, e.hora_inicio
            """
            cursor.execute(query, (año, mes))
            eventos = cursor.fetchall()
            cursor.close()
            return eventos
            
        except Exception as e:
            print(f"Error al obtener calendario mensual: {e}")
            return []
        finally:
            self.desconectar()