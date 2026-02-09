#!/usr/bin/env python3
"""
Test de conexión a la base de datos MySQL
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from database import DB_CONFIG, crear_conexion

def test_connection():
    """Probar la conexión a la base de datos"""
    print("🔍 Probando conexión a MySQL...")
    print("=" * 50)
    
    try:
        # Intentar conectar
        connection = crear_conexion()
        
        if connection and connection.is_connected():
            print("✅ Conexión exitosa a MySQL")
            
            # Obtener información del servidor
            db_info = connection.get_server_info()
            print(f"📊 Versión del servidor: {db_info}")
            
            cursor = connection.cursor()
            
            # Verificar base de datos
            cursor.execute("SELECT DATABASE()")
            database_name = cursor.fetchone()
            print(f"🗄️  Base de datos actual: {database_name[0] if database_name else 'Ninguna'}")
            
            # Listar tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"📋 Tablas encontradas ({len(tables)}):")
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"   - {table[0]}: {count} registros")
            else:
                print("⚠️  No se encontraron tablas en la base de datos")
            
            # Verificar usuarios
            try:
                cursor.execute("SELECT COUNT(*) FROM usuarios")
                user_count = cursor.fetchone()[0]
                print(f"👥 Usuarios registrados: {user_count}")
                
                if user_count > 0:
                    cursor.execute("SELECT nombre_usuario, tipo_usuario FROM usuarios")
                    users = cursor.fetchall()
                    print("📝 Lista de usuarios:")
                    for user in users:
                        print(f"   - {user[0]} ({user[1]})")
            except Error as e:
                print(f"⚠️  Tabla 'usuarios' no encontrada: {e}")
            
            cursor.close()
            connection.close()
            print("\n✅ Test de conexión completado exitosamente")
            return True
            
        else:
            print("❌ No se pudo establecer conexión")
            return False
            
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Posibles soluciones:")
        print("1. Verificar que MySQL esté ejecutándose")
        print("2. Comprobar credenciales en database.py")
        print("3. Asegurarse de que la base de datos 'gestion_escolar' exista")
        print("4. Verificar permisos del usuario MySQL")
        return False

def test_database_config():
    """Mostrar configuración actual"""
    print("\n⚙️  Configuración actual:")
    print("=" * 30)
    for key, value in DB_CONFIG.items():
        if key == 'password':
            print(f"{key}: {'*' * len(str(value)) if value else '(vacía)'}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    test_database_config()
    test_connection()