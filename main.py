#!/usr/bin/env python3
"""
GESJ - Plataforma de Gestión Educativa
Provincia de San Juan, República Argentina

Aplicación principal modularizada para la gestión escolar.
"""

import sys
import os

# Agregar el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Error al importar MainWindow: {e}")
    print("Verificando estructura de directorios...")
    
    # Verificar que existan los directorios y archivos necesarios
    if not os.path.exists('ui'):
        print("❌ Directorio 'ui' no encontrado")
    elif not os.path.exists('ui/__init__.py'):
        print("❌ Archivo 'ui/__init__.py' no encontrado")
    elif not os.path.exists('ui/main_window.py'):
        print("❌ Archivo 'ui/main_window.py' no encontrado")
    else:
        print("✅ Estructura de directorios parece correcta")
        print("Reintentando importación...")
        from ui.main_window import MainWindow

def main():
    """Función principal de la aplicación"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()