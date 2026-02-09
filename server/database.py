import mysql.connector
from mysql.connector import Error
import os

# Configuración de la base de datos MySQL
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'gestion_escolar',
    'user': 'root',  # Usuario por defecto de XAMPP
    'password': '',  # XAMPP por defecto no tiene contraseña
    'port': 3306
}

def crear_conexion():
    """Crea una conexión a la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def inicializar_base_datos():
    """Verifica que la base de datos esté disponible"""
    try:
        connection = crear_conexion()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            count = cursor.fetchone()[0]
            print(f"Base de datos conectada. {count} usuarios encontrados.")
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"Error al inicializar base de datos: {e}")
        return False
    return False

def crear_usuario(nombre, contrasena, rol):
    """Crea un usuario en la base de datos MySQL"""
    try:
        connection = crear_conexion()
        if connection:
            cursor = connection.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (nombre,))
            if cursor.fetchone():
                print(f"El usuario {nombre} ya existe")
                cursor.close()
                connection.close()
                return
            
            # Insertar nuevo usuario
            query = "INSERT INTO usuarios (nombre_usuario, contrasena, tipo_usuario) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, contrasena, rol))
            
            connection.commit()
            cursor.close()
            connection.close()
            print(f"Usuario {nombre} creado exitosamente con rol {rol}")
            
    except Error as e:
        print(f"Error al crear usuario: {e}")
        raise e

def verificar_usuario(nombre, contrasena):
    """Verifica las credenciales del usuario en MySQL"""
    try:
        connection = crear_conexion()
        if connection:
            cursor = connection.cursor()
            
            query = "SELECT tipo_usuario FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
            cursor.execute(query, (nombre, contrasena))
            
            resultado = cursor.fetchone()
            cursor.close()
            connection.close()
            
            return resultado
            
    except Error as e:
        print(f"Error al verificar usuario: {e}")
        return None

def obtener_todos_usuarios():
    """Obtiene todos los usuarios de la base de datos MySQL"""
    try:
        connection = crear_conexion()
        if connection:
            cursor = connection.cursor()
            
            cursor.execute("SELECT nombre_usuario, tipo_usuario, 'No especificado' as email FROM usuarios")
            usuarios = cursor.fetchall()
            
            cursor.close()
            connection.close()
            return usuarios
            
    except Error as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def obtener_usuario_por_nombre(nombre):
    """Obtiene un usuario específico por nombre"""
    try:
        connection = crear_conexion()
        if connection:
            cursor = connection.cursor()
            
            query = "SELECT id, nombre_usuario, tipo_usuario FROM usuarios WHERE nombre_usuario = %s"
            cursor.execute(query, (nombre,))
            
            resultado = cursor.fetchone()
            cursor.close()
            connection.close()
            
            return resultado
            
    except Error as e:
        print(f"Error al obtener usuario: {e}")
        return None

# Función para verificar si un usuario tiene un rol específico
def verificar_rol_usuario(nombre, rol_requerido):
    """Verifica si un usuario tiene un rol específico"""
    try:
        connection = crear_conexion()
        if connection:
            cursor = connection.cursor()
            
            query = "SELECT tipo_usuario FROM usuarios WHERE nombre_usuario = %s"
            cursor.execute(query, (nombre,))
            
            resultado = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if resultado and resultado[0] == rol_requerido:
                return True
            return False
            
    except Error as e:
        print(f"Error al verificar rol: {e}")
        return False

# Inicializar la base de datos al importar el módulo
if __name__ == "__main__":
    inicializar_base_datos()