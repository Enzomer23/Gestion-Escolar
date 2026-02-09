#!/usr/bin/env python3
"""
Script de configuración para el sistema de calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import mysql.connector
from mysql.connector import Error
from database import DB_CONFIG

def ejecutar_script_sql(archivo_sql):
    """Ejecutar un archivo SQL en la base de datos"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Leer el archivo SQL
        with open(archivo_sql, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Dividir en comandos individuales
        comandos = sql_script.split(';')
        
        for comando in comandos:
            comando = comando.strip()
            if comando and not comando.startswith('--'):
                try:
                    cursor.execute(comando)
                    connection.commit()
                except Error as e:
                    if "already exists" not in str(e).lower():
                        print(f"Error ejecutando comando: {e}")
                        print(f"Comando: {comando[:100]}...")
        
        cursor.close()
        connection.close()
        print(f"✅ Script {archivo_sql} ejecutado correctamente")
        return True
        
    except Error as e:
        print(f"❌ Error ejecutando {archivo_sql}: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Archivo {archivo_sql} no encontrado")
        return False

def verificar_instalacion():
    """Verificar que las tablas se crearon correctamente"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Verificar tablas principales
        tablas_requeridas = [
            'alumnos', 'materias', 'calificaciones', 
            'periodos_evaluacion', 'tipos_evaluacion', 'promedios_alumnos'
        ]
        
        for tabla in tablas_requeridas:
            cursor.execute(f"SHOW TABLES LIKE '{tabla}'")
            if cursor.fetchone():
                print(f"✅ Tabla '{tabla}' creada correctamente")
            else:
                print(f"❌ Tabla '{tabla}' no encontrada")
        
        # Verificar datos de ejemplo
        cursor.execute("SELECT COUNT(*) FROM alumnos")
        count_alumnos = cursor.fetchone()[0]
        print(f"📊 Alumnos registrados: {count_alumnos}")
        
        cursor.execute("SELECT COUNT(*) FROM materias")
        count_materias = cursor.fetchone()[0]
        print(f"📚 Materias registradas: {count_materias}")
        
        cursor.execute("SELECT COUNT(*) FROM calificaciones")
        count_calificaciones = cursor.fetchone()[0]
        print(f"📝 Calificaciones registradas: {count_calificaciones}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error verificando instalación: {e}")

def main():
    """Función principal de configuración"""
    print("🚀 Configurando Sistema de Calificaciones GESJ")
    print("=" * 50)
    
    # Ejecutar script de calificaciones
    if ejecutar_script_sql('calificaciones_schema.sql'):
        print("\n🔍 Verificando instalación...")
        verificar_instalacion()
        print("\n✅ Sistema de calificaciones configurado correctamente!")
        print("\n📋 Próximos pasos:")
        print("1. Ejecutar la aplicación: python main.py")
        print("2. Iniciar sesión como docente (usuario: docente1, contraseña: abcd)")
        print("3. Acceder a 'Gestionar Calificaciones'")
    else:
        print("\n❌ Error en la configuración. Revise los mensajes anteriores.")

if __name__ == "__main__":
    main()