"""
ARCHIVO DE COMPATIBILIDAD - Importaciones del Sistema Modular
GESJ - Plataforma de Gestión Educativa

Este archivo mantiene compatibilidad con importaciones existentes
redirigiendo al nuevo sistema modular.
"""

# Importar desde el nuevo sistema modular
from .calificaciones.manager import CalificacionesManager

# Mantener compatibilidad con importaciones existentes
__all__ = ['CalificacionesManager']

# Mensaje informativo
print("✅ Usando sistema modular de calificaciones")