"""
ARCHIVO PRINCIPAL DEL MÓDULO DE CALIFICACIONES
GESJ - Plataforma de Gestión Educativa
Provincia de San Juan, República Argentina

Este archivo expone las clases principales del sistema de calificaciones
para mantener compatibilidad con las importaciones existentes.
"""

# Importar desde el sistema modular
from .calificaciones.manager import CalificacionesManager
from .calificaciones.alumnos import AlumnosOperations
from .calificaciones.materias import MateriasOperations
from .calificaciones.evaluaciones import EvaluacionesOperations
from .calificaciones.promedios import PromediosOperations
from .calificaciones.estadisticas import EstadisticasOperations
from .calificaciones.reportes import ReportesOperations

# Exportar las clases principales para compatibilidad
__all__ = [
    'CalificacionesManager',
    'AlumnosOperations',
    'MateriasOperations',
    'EvaluacionesOperations', 
    'PromediosOperations',
    'EstadisticasOperations',
    'ReportesOperations'
]

# Mensaje informativo
print("✅ Módulo de calificaciones cargado correctamente")