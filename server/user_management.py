"""
Gestión Avanzada de Usuarios
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import List, Dict, Optional
from .database import crear_conexion

class UserManager:
    """Gestor avanzado de usuarios del sistema"""
    
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
    
    def crear_usuario(self, nombre_usuario: str, contrasena: str, tipo_usuario: str, 
                     email: str = None) -> bool:
        """Crear nuevo usuario en el sistema"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            if cursor.fetchone():
                print(f"El usuario {nombre_usuario} ya existe")
                cursor.close()
                return False
            
            # Insertar nuevo usuario
            query = "INSERT INTO usuarios (nombre_usuario, contrasena, tipo_usuario) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre_usuario, contrasena, tipo_usuario))
            
            self.connection.commit()
            cursor.close()
            print(f"Usuario {nombre_usuario} creado exitosamente con rol {tipo_usuario}")
            return True
            
        except Error as e:
            print(f"Error al crear usuario: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def actualizar_usuario(self, nombre_usuario: str, nuevos_datos: Dict) -> bool:
        """Actualizar datos de un usuario existente"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            
            # Construir query dinámicamente según los datos a actualizar
            campos_actualizar = []
            valores = []
            
            if 'contrasena' in nuevos_datos and nuevos_datos['contrasena']:
                campos_actualizar.append("contrasena = %s")
                valores.append(nuevos_datos['contrasena'])
            
            if 'tipo_usuario' in nuevos_datos:
                campos_actualizar.append("tipo_usuario = %s")
                valores.append(nuevos_datos['tipo_usuario'])
            
            if not campos_actualizar:
                print("No hay campos para actualizar")
                cursor.close()
                return False
            
            # Agregar nombre de usuario para WHERE
            valores.append(nombre_usuario)
            
            query = f"UPDATE usuarios SET {', '.join(campos_actualizar)} WHERE nombre_usuario = %s"
            cursor.execute(query, valores)
            
            if cursor.rowcount > 0:
                self.connection.commit()
                print(f"Usuario {nombre_usuario} actualizado exitosamente")
                result = True
            else:
                print(f"Usuario {nombre_usuario} no encontrado")
                result = False
            
            cursor.close()
            return result
            
        except Error as e:
            print(f"Error al actualizar usuario: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def eliminar_usuario(self, nombre_usuario: str) -> bool:
        """Eliminar usuario del sistema"""
        try:
            if not self.conectar():
                return False
            
            cursor = self.connection.cursor()
            
            # Verificar que no sea un usuario crítico
            if nombre_usuario in ['admin1', 'admin']:
                print(f"No se puede eliminar el usuario crítico: {nombre_usuario}")
                cursor.close()
                return False
            
            # Eliminar usuario
            cursor.execute("DELETE FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            
            if cursor.rowcount > 0:
                self.connection.commit()
                print(f"Usuario {nombre_usuario} eliminado exitosamente")
                result = True
            else:
                print(f"Usuario {nombre_usuario} no encontrado")
                result = False
            
            cursor.close()
            return result
            
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.desconectar()
    
    def obtener_usuario_por_nombre(self, nombre_usuario: str) -> Optional[Dict]:
        """Obtener información completa de un usuario"""
        try:
            if not self.conectar():
                return None
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, nombre_usuario, tipo_usuario, fecha_creacion
                FROM usuarios 
                WHERE nombre_usuario = %s
            """
            cursor.execute(query, (nombre_usuario,))
            usuario = cursor.fetchone()
            cursor.close()
            return usuario
            
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            self.desconectar()
    
    def listar_usuarios_por_tipo(self, tipo_usuario: str) -> List[Dict]:
        """Listar usuarios por tipo específico"""
        try:
            if not self.conectar():
                return []
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, nombre_usuario, tipo_usuario, fecha_creacion
                FROM usuarios 
                WHERE tipo_usuario = %s
                ORDER BY nombre_usuario
            """
            cursor.execute(query, (tipo_usuario,))
            usuarios = cursor.fetchall()
            cursor.close()
            return usuarios
            
        except Error as e:
            print(f"Error al listar usuarios por tipo: {e}")
            return []
        finally:
            self.desconectar()
    
    def cambiar_contrasena(self, nombre_usuario: str, nueva_contrasena: str) -> bool:
        """Cambiar contraseña de un usuario"""
        return self.actualizar_usuario(nombre_usuario, {'contrasena': nueva_contrasena})
    
    def cambiar_rol(self, nombre_usuario: str, nuevo_rol: str) -> bool:
        """Cambiar rol de un usuario"""
        return self.actualizar_usuario(nombre_usuario, {'tipo_usuario': nuevo_rol})
    
    def obtener_estadisticas_usuarios(self) -> Dict:
        """Obtener estadísticas generales de usuarios"""
        try:
            if not self.conectar():
                return {}
            
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    COUNT(*) as total_usuarios,
                    COUNT(CASE WHEN tipo_usuario = 'Padre' THEN 1 END) as total_padres,
                    COUNT(CASE WHEN tipo_usuario = 'Docente' THEN 1 END) as total_docentes,
                    COUNT(CASE WHEN tipo_usuario = 'Preceptor' THEN 1 END) as total_preceptores,
                    COUNT(CASE WHEN tipo_usuario = 'Administrativo' THEN 1 END) as total_administrativos
                FROM usuarios
            """
            cursor.execute(query)
            estadisticas = cursor.fetchone()
            cursor.close()
            return estadisticas or {}
            
        except Error as e:
            print(f"Error al obtener estadísticas de usuarios: {e}")
            return {}
        finally:
            self.desconectar()