#!/usr/bin/env python3
"""
Script de verificación de importaciones
GESJ - Plataforma de Gestión Educativa
"""

print("🔍 VERIFICANDO IMPORTACIONES DEL SISTEMA GESJ...")
print("=" * 60)

try:
    print("📦 Importando ui.main_window...")
    from ui.main_window import MainWindow
    print("✅ MainWindow importado correctamente")
    
    print("📦 Importando ui.auth...")
    from ui.auth import AuthManager
    print("✅ AuthManager importado correctamente")
    
    print("📦 Importando secciones...")
    from ui.sections.padres import PadresSection
    print("✅ PadresSection importado correctamente")
    
    from ui.sections.docentes import DocentesSection
    print("✅ DocentesSection importado correctamente")
    
    from ui.sections.preceptores import PreceptoresSection
    print("✅ PreceptoresSection importado correctamente")
    
    from ui.sections.administradores import AdministradoresSection
    print("✅ AdministradoresSection importado correctamente")
    
    print("📦 Importando calificaciones_docente...")
    from ui.sections.calificaciones_docente import CalificacionesDocenteWindow
    print("✅ CalificacionesDocenteWindow importado correctamente")
    
    print("\n🎉 ¡TODAS LAS IMPORTACIONES EXITOSAS!")
    print("=" * 60)
    print("✅ El sistema GESJ está listo para funcionar")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("🔧 Revisa que todos los archivos estén en su lugar")
    
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
    print("🔧 Hay errores de sintaxis que necesitan arreglarse")
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    print("🔧 Revisa la configuración del sistema")

print("\n🚀 Para ejecutar el sistema completo:")
print("   python main.py")