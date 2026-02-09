"""
Operaciones de base de datos para el sistema de calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from .database import crear_conexion

class CalificacionesManager:
    """Gestor de operaciones de calificaciones en la base de datos"""
    
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
    
    # OPERACIONES DE ALUMNOS
    def obtener_alumnos_por_curso(self, curso: str, division: str = 'A') -> List[Dict]:
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
    
    def obtener_alumno_por_id(self, alumno_id: int) -> Optional[Dict]:
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
    
    # OPERACIONES DE MATERIAS
    def obtener_materias_por_docente(self, docente_id: int) -> List[Dict]:
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
    
    def obtener_materias_por_curso(self, curso: str, division: str = 'A') -> List[Dict]:
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
    
    # OPERACIONES DE PERÍODOS Y TIPOS DE EVALUACIÓN
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
    
    # OPERACIONES DE CALIFICACIONES
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
            
            # Actualizar promedios (versión simplificada)
            self.actualizar_promedios_simple(alumno_id, materia_id, periodo_id)
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
                        c.id,
                        c.alumno_id,
                        c.materia_id,
                        c.periodo_id,
                        c.tipo_evaluacion_id,
                        CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                        a.curso,
                        a.division,
                        m.nombre AS materia,
                        m.codigo AS codigo_materia,
                        u.nombre_usuario AS docente,
                        p.nombre AS periodo,
                        te.nombre AS tipo_evaluacion,
                        c.nota,
                        c.fecha_evaluacion,
                        c.observaciones,
                        c.fecha_registro
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN materias m ON c.materia_id = m.id
                    JOIN usuarios u ON c.docente_id = u.id
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    JOIN tipos_evaluacion te ON c.tipo_evaluacion_id = te.id
                    WHERE c.alumno_id = %s AND c.periodo_id = %s AND a.activo = TRUE AND m.activa = TRUE
                    ORDER BY m.nombre, c.fecha_evaluacion
                """
                cursor.execute(query, (alumno_id, periodo_id))
            else:
                query = """
                    SELECT 
                        c.id,
                        c.alumno_id,
                        c.materia_id,
                        c.periodo_id,
                        c.tipo_evaluacion_id,
                        CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                        a.curso,
                        a.division,
                        m.nombre AS materia,
                        m.codigo AS codigo_materia,
                        u.nombre_usuario AS docente,
                        p.nombre AS periodo,
                        te.nombre AS tipo_evaluacion,
                        c.nota,
                        c.fecha_evaluacion,
                        c.observaciones,
                        c.fecha_registro
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
                    c.id,
                    c.alumno_id,
                    c.materia_id,
                    c.periodo_id,
                    c.tipo_evaluacion_id,
                    CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                    a.curso,
                    a.division,
                    m.nombre AS materia,
                    m.codigo AS codigo_materia,
                    u.nombre_usuario AS docente,
                    p.nombre AS periodo,
                    te.nombre AS tipo_evaluacion,
                    c.nota,
                    c.fecha_evaluacion,
                    c.observaciones,
                    c.fecha_registro
                FROM calificaciones c
                JOIN alumnos a ON c.alumno_id = a.id
                JOIN materias m ON c.materia_id = m.id
                JOIN usuarios u ON c.docente_id = u.id
                JOIN periodos_evaluacion p ON c.periodo_id = p.id
                JOIN tipos_evaluacion te ON c.tipo_evaluacion_id = te.id
                WHERE c.materia_id = %s AND c.periodo_id = %s AND a.activo = TRUE AND m.activa = TRUE
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
                        a.curso,
                        a.division,
                        m.id AS materia_id,
                        m.nombre AS materia,
                        p.id AS periodo_id,
                        p.nombre AS periodo,
                        ROUND(AVG(c.nota), 2) AS promedio,
                        COUNT(c.nota) AS cantidad_notas
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN materias m ON c.materia_id = m.id
                    JOIN periodos_evaluacion p ON c.periodo_id = p.id
                    WHERE c.alumno_id = %s AND c.periodo_id = %s AND a.activo = TRUE AND m.activa = TRUE
                    GROUP BY a.id, m.id, p.id
                    ORDER BY m.nombre
                """
                cursor.execute(query, (alumno_id, periodo_id))
            else:
                query = """
                    SELECT 
                        a.id AS alumno_id,
                        CONCAT(a.apellido, ', ', a.nombre) AS alumno,
                        a.curso,
                        a.division,
                        m.id AS materia_id,
                        m.nombre AS materia,
                        p.id AS periodo_id,
                        p.nombre AS periodo,
                        ROUND(AVG(c.nota), 2) AS promedio,
                        COUNT(c.nota) AS cantidad_notas
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
    
    def obtener_promedio_general_alumno(self, alumno_id: int, periodo_id: int) -> float:
        """Obtener promedio general de un alumno en un período"""
        try:
            if not self.conectar():
                return 0.0
            
            cursor = self.connection.cursor()
            query = "SELECT PromedioGeneralAlumno(%s, %s) as promedio"
            cursor.execute(query, (alumno_id, periodo_id))
            resultado = cursor.fetchone()
            cursor.close()
            
            return float(resultado[0]) if resultado and resultado[0] else 0.0
            
        except Error as e:
            print(f"Error al obtener promedio general: {e}")
            return 0.0
        finally:
            self.desconectar()
    
    def actualizar_promedios(self):
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
                self.actualizar_promedios_manual()
            
            cursor.close()
            return True
            
        except Error as e:
            print(f"Error al actualizar promedios: {e}")
            return False
        finally:
            self.desconectar()
    
    def actualizar_promedios_simple(self, alumno_id: int, materia_id: int, periodo_id: int):
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
                
                # Usar solo las columnas básicas que sabemos que existen
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
    
    def actualizar_promedios_manual(self):
        """Actualizar promedios manualmente si no existe el procedimiento"""
        try:
            cursor = self.connection.cursor()
            
            # Limpiar tabla de promedios
            cursor.execute("DELETE FROM promedios_alumnos")
            
            # Insertar solo columnas básicas que sabemos que existen
            cursor.execute("""
                INSERT INTO promedios_alumnos (alumno_id, materia_id, periodo_id, promedio, cantidad_notas)
                SELECT 
                    alumno_id,
                    materia_id,
                    periodo_id,
                    ROUND(AVG(nota), 2) as promedio,
                    COUNT(*) as cantidad_notas
                FROM calificaciones
                GROUP BY alumno_id, materia_id, periodo_id
            """)
            
            self.connection.commit()
            
        except Error as e:
            print(f"Error en actualización manual de promedios: {e}")
            raise e
    
    # REPORTES Y ESTADÍSTICAS
    def obtener_estadisticas_curso(self, curso: str, division: str, periodo_id: int) -> Dict:
        """Obtener estadísticas generales de un curso"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            
            # Promedio general del curso
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
                    a.curso,
                    a.division,
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