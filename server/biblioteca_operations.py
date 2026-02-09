"""
Operaciones de base de datos para el módulo de biblioteca
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from .database import crear_conexion

class BibliotecaManager:
    """Gestor de operaciones de biblioteca en la base de datos"""
    
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
    
    def obtener_libros_disponibles(self, categoria: str = None) -> List[Dict]:
        """Obtener libros disponibles en la biblioteca"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if categoria:
                query = """
                    SELECT 
                        l.id,
                        l.titulo,
                        l.autor,
                        l.isbn,
                        l.categoria,
                        l.editorial,
                        l.año_publicacion,
                        l.cantidad_total,
                        l.cantidad_disponible,
                        l.ubicacion
                    FROM libros l
                    WHERE l.activo = TRUE AND l.categoria = %s
                    ORDER BY l.titulo
                """
                cursor.execute(query, (categoria,))
            else:
                query = """
                    SELECT 
                        l.id,
                        l.titulo,
                        l.autor,
                        l.isbn,
                        l.categoria,
                        l.editorial,
                        l.año_publicacion,
                        l.cantidad_total,
                        l.cantidad_disponible,
                        l.ubicacion
                    FROM libros l
                    WHERE l.activo = TRUE
                    ORDER BY l.categoria, l.titulo
                """
                cursor.execute(query)
            
            libros = cursor.fetchall()
            cursor.close()
            return libros
            
        except Error as e:
            print(f"Error al obtener libros: {e}")
            return []
        finally:
            self.desconectar()
    
    def registrar_prestamo(self, libro_id: int, alumno_id: int, docente_id: int,
                          fecha_prestamo: date = None, dias_prestamo: int = 7) -> bool:
        """Registrar un préstamo de libro"""
        try:
            if not self.conectar():
                return False
            
            if not fecha_prestamo:
                fecha_prestamo = date.today()
            
            fecha_devolucion = fecha_prestamo + timedelta(days=dias_prestamo)
            
            cursor = self.connection.cursor()
            
            # Verificar disponibilidad
            cursor.execute("SELECT cantidad_disponible FROM libros WHERE id = %s", (libro_id,))
            resultado = cursor.fetchone()
            
            if not resultado or resultado[0] <= 0:
                cursor.close()
                return False
            
            # Registrar préstamo
            query = """
                INSERT INTO prestamos_biblioteca 
                (libro_id, alumno_id, docente_autoriza, fecha_prestamo, fecha_devolucion_esperada, estado)
                VALUES (%s, %s, %s, %s, %s, 'Activo')
            """
            cursor.execute(query, (libro_id, alumno_id, docente_id, fecha_prestamo, fecha_devolucion))
            
            # Actualizar cantidad disponible
            cursor.execute("""
                UPDATE libros 
                SET cantidad_disponible = cantidad_disponible - 1 
                WHERE id = %s
            """, (libro_id,))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            print(f"Error al registrar préstamo: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_prestamos_activos(self, alumno_id: int = None) -> List[Dict]:
        """Obtener préstamos activos"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if alumno_id:
                query = """
                    SELECT 
                        p.id,
                        l.titulo,
                        l.autor,
                        CONCAT(a.apellido, ', ', a.nombre) as alumno,
                        p.fecha_prestamo,
                        p.fecha_devolucion_esperada,
                        DATEDIFF(p.fecha_devolucion_esperada, CURDATE()) as dias_restantes,
                        p.estado
                    FROM prestamos_biblioteca p
                    JOIN libros l ON p.libro_id = l.id
                    JOIN alumnos a ON p.alumno_id = a.id
                    WHERE p.alumno_id = %s AND p.estado = 'Activo'
                    ORDER BY p.fecha_devolucion_esperada
                """
                cursor.execute(query, (alumno_id,))
            else:
                query = """
                    SELECT 
                        p.id,
                        l.titulo,
                        l.autor,
                        CONCAT(a.apellido, ', ', a.nombre) as alumno,
                        a.curso,
                        a.division,
                        p.fecha_prestamo,
                        p.fecha_devolucion_esperada,
                        DATEDIFF(p.fecha_devolucion_esperada, CURDATE()) as dias_restantes,
                        p.estado
                    FROM prestamos_biblioteca p
                    JOIN libros l ON p.libro_id = l.id
                    JOIN alumnos a ON p.alumno_id = a.id
                    WHERE p.estado = 'Activo'
                    ORDER BY p.fecha_devolucion_esperada
                """
                cursor.execute(query)
            
            prestamos = cursor.fetchall()
            cursor.close()
            return prestamos
            
        except Error as e:
            print(f"Error al obtener préstamos activos: {e}")
            return []
        finally:
            self.desconectar()
    
    def devolver_libro(self, prestamo_id: int, fecha_devolucion: date = None, 
                      observaciones: str = "") -> bool:
        """Registrar devolución de un libro"""
        try:
            if not self.conectar():
                return False
            
            if not fecha_devolucion:
                fecha_devolucion = date.today()
            
            cursor = self.connection.cursor()
            
            # Obtener información del préstamo
            cursor.execute("""
                SELECT libro_id, fecha_devolucion_esperada 
                FROM prestamos_biblioteca 
                WHERE id = %s AND estado = 'Activo'
            """, (prestamo_id,))
            
            prestamo_info = cursor.fetchone()
            if not prestamo_info:
                cursor.close()
                return False
            
            libro_id, fecha_esperada = prestamo_info
            
            # Determinar si hay multa por retraso
            multa = 0
            if fecha_devolucion > fecha_esperada:
                dias_retraso = (fecha_devolucion - fecha_esperada).days
                multa = dias_retraso * 50  # $50 por día de retraso
            
            # Actualizar préstamo
            cursor.execute("""
                UPDATE prestamos_biblioteca 
                SET estado = 'Devuelto',
                    fecha_devolucion_real = %s,
                    observaciones_devolucion = %s,
                    multa = %s
                WHERE id = %s
            """, (fecha_devolucion, observaciones, multa, prestamo_id))
            
            # Actualizar cantidad disponible del libro
            cursor.execute("""
                UPDATE libros 
                SET cantidad_disponible = cantidad_disponible + 1 
                WHERE id = %s
            """, (libro_id,))
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            print(f"Error al devolver libro: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_estadisticas_biblioteca(self) -> Dict:
        """Obtener estadísticas generales de la biblioteca"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            
            # Estadísticas generales
            query = """
                SELECT 
                    COUNT(*) as total_libros,
                    SUM(cantidad_total) as total_ejemplares,
                    SUM(cantidad_disponible) as ejemplares_disponibles,
                    COUNT(DISTINCT categoria) as total_categorias
                FROM libros 
                WHERE activo = TRUE
            """
            cursor.execute(query)
            stats_libros = cursor.fetchone()
            
            # Estadísticas de préstamos
            cursor.execute("""
                SELECT 
                    COUNT(*) as prestamos_activos,
                    COUNT(CASE WHEN fecha_devolucion_esperada < CURDATE() THEN 1 END) as prestamos_vencidos
                FROM prestamos_biblioteca 
                WHERE estado = 'Activo'
            """)
            stats_prestamos = cursor.fetchone()
            
            cursor.close()
            
            # Combinar estadísticas
            estadisticas = {**stats_libros, **stats_prestamos}
            return estadisticas
            
        except Error as e:
            print(f"Error al obtener estadísticas de biblioteca: {e}")
            return {}
        finally:
            self.desconectar()