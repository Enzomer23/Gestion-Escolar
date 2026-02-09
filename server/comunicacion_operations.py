"""
Operaciones de base de datos para el módulo de comunicación avanzada
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import List, Dict, Optional
from .database import crear_conexion

class ComunicacionManager:
    """Gestor de operaciones de comunicación en la base de datos"""
    
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
    
    def enviar_mensaje(self, remitente_id: int, destinatario_id: int, asunto: str,
                      mensaje: str, tipo_mensaje: str = "Personal") -> bool:
        """Enviar un mensaje entre usuarios"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            query = """
                INSERT INTO mensajes_internos 
                (remitente_id, destinatario_id, asunto, mensaje, tipo_mensaje, estado)
                VALUES (%s, %s, %s, %s, %s, 'Enviado')
            """
            cursor.execute(query, (remitente_id, destinatario_id, asunto, mensaje, tipo_mensaje))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_mensajes_usuario(self, usuario_id: int, tipo: str = "recibidos") -> List[Dict]:
        """Obtener mensajes de un usuario"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if tipo == "recibidos":
                query = """
                    SELECT 
                        m.id,
                        m.asunto,
                        m.mensaje,
                        m.fecha_envio,
                        m.leido,
                        m.tipo_mensaje,
                        ur.nombre_usuario as remitente,
                        ur.tipo_usuario as tipo_remitente
                    FROM mensajes_internos m
                    JOIN usuarios ur ON m.remitente_id = ur.id
                    WHERE m.destinatario_id = %s
                    ORDER BY m.fecha_envio DESC
                """
            else:  # enviados
                query = """
                    SELECT 
                        m.id,
                        m.asunto,
                        m.mensaje,
                        m.fecha_envio,
                        m.leido,
                        m.tipo_mensaje,
                        ud.nombre_usuario as destinatario,
                        ud.tipo_usuario as tipo_destinatario
                    FROM mensajes_internos m
                    JOIN usuarios ud ON m.destinatario_id = ud.id
                    WHERE m.remitente_id = %s
                    ORDER BY m.fecha_envio DESC
                """
            
            cursor.execute(query, (usuario_id,))
            mensajes = cursor.fetchall()
            cursor.close()
            return mensajes
            
        except Exception as e:
            print(f"Error al obtener mensajes: {e}")
            return []
        finally:
            self.desconectar()
    
    def crear_anuncio_institucional(self, titulo: str, contenido: str, autor_id: int,
                                   dirigido_a: str = "Toda la comunidad", 
                                   prioridad: str = "Normal") -> bool:
        """Crear un anuncio institucional"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            query = """
                INSERT INTO anuncios_institucionales 
                (titulo, contenido, autor_id, dirigido_a, prioridad, estado)
                VALUES (%s, %s, %s, %s, %s, 'Publicado')
            """
            cursor.execute(query, (titulo, contenido, autor_id, dirigido_a, prioridad))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            print(f"Error al crear anuncio: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_anuncios_activos(self, dirigido_a: str = None) -> List[Dict]:
        """Obtener anuncios institucionales activos"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if dirigido_a:
                query = """
                    SELECT 
                        a.id,
                        a.titulo,
                        a.contenido,
                        a.fecha_publicacion,
                        a.prioridad,
                        u.nombre_usuario as autor
                    FROM anuncios_institucionales a
                    JOIN usuarios u ON a.autor_id = u.id
                    WHERE a.estado = 'Publicado' 
                    AND (a.dirigido_a = %s OR a.dirigido_a = 'Toda la comunidad')
                    ORDER BY a.prioridad DESC, a.fecha_publicacion DESC
                """
                cursor.execute(query, (dirigido_a,))
            else:
                query = """
                    SELECT 
                        a.id,
                        a.titulo,
                        a.contenido,
                        a.fecha_publicacion,
                        a.prioridad,
                        a.dirigido_a,
                        u.nombre_usuario as autor
                    FROM anuncios_institucionales a
                    JOIN usuarios u ON a.autor_id = u.id
                    WHERE a.estado = 'Publicado'
                    ORDER BY a.prioridad DESC, a.fecha_publicacion DESC
                """
                cursor.execute(query)
            
            anuncios = cursor.fetchall()
            cursor.close()
            return anuncios
            
        except Exception as e:
            print(f"Error al obtener anuncios: {e}")
            return []
        finally:
            self.desconectar()