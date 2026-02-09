"""
Operaciones de Promedios para el Sistema de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
from ..database import crear_conexion

class PromediosOperations:
    """Operaciones especializadas para cálculo y gestión de promedios"""
    
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
    
    def obtener_promedios_alumno(self, alumno_id: int, periodo_id: int = None) -> List[Dict]:
        """Obtener promedios de un alumno"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            
            if periodo_id:
                query = """
                    SELECT 
                        a.id AS alumno_id,
                        CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                        a.curso, a.division,
                        m.id AS materia_id, m.nombre AS materia,
                        p.id AS periodo_id, p.nombre AS periodo,
                        ROUND(AVG(c.nota), 2) AS promedio,
                        COUNT(c.nota) AS cantidad_notas,
                        MIN(c.nota) AS nota_min_calc,
                        MAX(c.nota) AS nota_max_calc
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN materias m ON c.materia_id = m.id
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    WHERE c.alumno_id = %s AND c.periodo_id = %s 
                    AND a.activo = TRUE AND m.activa = TRUE
                    GROUP BY a.id, m.id, p.id
                    ORDER BY m.nombre
                """
                cursor.execute(query, (alumno_id, periodo_id))
            else:
                query = """
                    SELECT 
                        a.id AS alumno_id,
                        CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                        a.curso, a.division,
                        m.id AS materia_id, m.nombre AS materia,
                        p.id AS periodo_id, p.nombre AS periodo,
                        ROUND(AVG(c.nota), 2) AS promedio,
                        COUNT(c.nota) AS cantidad_notas,
                        MIN(c.nota) AS nota_min_calc,
                        MAX(c.nota) AS nota_max_calc
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN materias m ON c.materia_id = m.id
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    WHERE c.alumno_id = %s AND a.activo = TRUE AND m.activa = TRUE
                    GROUP BY a.id, m.id, p.id
                    ORDER BY p.nombre, m.nombre
                """
                cursor.execute(query, (alumno_id,))
            
            promedios = cursor.fetchall()
            cursor.close()
            return promedios
            
        except Error as e:
            print(f"Error al obtener promedios del alumno: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_promedio_general(self, alumno_id: int, periodo_id: int) -> float:
        """Obtener promedio general de un alumno en un período"""
        try:
            if not self.conectar():
                return 0.0
            
            cursor = self.connection.cursor()
            
            # Intentar usar la función si existe
            try:
                query = "SELECT PromedioGeneralAlumno(%s, %s) as promedio"
                cursor.execute(query, (alumno_id, periodo_id))
                resultado = cursor.fetchone()
                if resultado and resultado[0]:
                    cursor.close()
                    return float(resultado[0])
            except Error:
                pass
            
            # Método alternativo si no existe la función
            query = """
                SELECT ROUND(AVG(nota), 2) as promedio
                FROM calificaciones
                WHERE alumno_id = %s AND periodo_id = %s
            """
            cursor.execute(query, (alumno_id, periodo_id))
            resultado = cursor.fetchone()
            cursor.close()
            
            return float(resultado[0]) if resultado and resultado[0] else 0.0
            
        except Error as e:
            print(f"Error al obtener promedio general: {e}")
            return 0.0
        finally:
            self.desconectar()
    
    def actualizar_todos(self):
        """Actualizar tabla de promedios calculados"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            
            # Verificar si existe la tabla promedios_alumnos
            cursor.execute("SHOW TABLES LIKE 'promedios_alumnos'")
            if not cursor.fetchone():
                print("Tabla promedios_alumnos no existe, saltando actualización")
                cursor.close()
                return True
            
            # Verificar si existe el procedimiento
            cursor.execute("SHOW PROCEDURE STATUS WHERE Name = 'CalcularPromedios'")
            if cursor.fetchone():
                cursor.callproc('CalcularPromedios')
                self.connection.commit()
            else:
                print("Procedimiento CalcularPromedios no existe, usando método alternativo")
                self.actualizar_manual()
            
            cursor.close()
            return True
            
        except Error as e:
            print(f"Error al actualizar promedios: {e}")
            return False
        finally:
            self.desconectar()
    
    def actualizar_simple(self, alumno_id: int, materia_id: int, periodo_id: int):
        """Actualizar promedio específico de un alumno en una materia"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            
            # Verificar si existe la tabla promedios_alumnos
            cursor.execute("SHOW TABLES LIKE 'promedios_alumnos'")
            if not cursor.fetchone():
                cursor.close()
                return True
            
            # Calcular promedio
            cursor.execute("""
                SELECT 
                    ROUND(AVG(nota), 2) as promedio,
                    COUNT(*) as cantidad_notas
                FROM calificaciones 
                WHERE alumno_id = %s AND materia_id = %s AND periodo_id = %s
            """, (alumno_id, materia_id, periodo_id))
            
            resultado = cursor.fetchone()
            if resultado:
                promedio, cantidad = resultado
                
                cursor.execute("""
                    INSERT INTO promedios_alumnos 
                    (alumno_id, materia_id, periodo_id, promedio, cantidad_notas)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    promedio = VALUES(promedio),
                    cantidad_notas = VALUES(cantidad_notas)
                """, (alumno_id, materia_id, periodo_id, promedio, cantidad))
                
                self.connection.commit()
            
            cursor.close()
            return True
            
        except Error as e:
            print(f"Error al actualizar promedio simple: {e}")
            return False
        finally:
            self.desconectar()
    
    def actualizar_manual(self):
        """Actualizar promedios manualmente si no existe el procedimiento"""
        try:
            cursor = self.connection.cursor()
            
            # Limpiar tabla de promedios
            cursor.execute("DELETE FROM promedios_alumnos")
            
            # Insertar promedios calculados
            cursor.execute("""
                INSERT INTO promedios_alumnos (alumno_id, materia_id, periodo_id, promedio, cantidad_notas)
                SELECT 
                    alumno_id, materia_id, periodo_id,
                    ROUND(AVG(nota), 2) as promedio,
                    COUNT(*) as cantidad_notas
                FROM calificaciones
                GROUP BY alumno_id, materia_id, periodo_id
            """)
            
            self.connection.commit()
            
        except Error as e:
            print(f"Error en actualización manual de promedios: {e}")
            raise e